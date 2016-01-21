#include "nomadmodel.h"

static Pedestrian * pedestrians;
static Wall * walls;
static Py_ssize_t a_count;
static Py_ssize_t escaped_count;

static double timestep;

static Py_ssize_t fline_c;

static Wall * flowlines;
static Py_ssize_t *new_flow_c;


static void update_total_count(Py_ssize_t count)
{
	if(count == a_count) return;
	a_count = count;
	pedestrians = PyMem_Realloc(pedestrians, a_count * sizeof(Pedestrian));
}

static PyObject* get_total_count(PyObject* self)
{
	return PyFloat_FromDouble(a_count);
}

static PyObject* get_escaped_count(PyObject* self)
{
	return PyFloat_FromDouble(escaped_count);
}

static double double_from_attribute(PyObject * o, char * name)
{
    PyObject * o2 = PyDict_GetItemString(o, name);
    double result = PyFloat_AsDouble(o2);
    return result;
}

static Vector vector_from_pyobject(PyObject * o)
{
    Vector v;

    PyObject * x = PySequence_GetItem(o, 0);
    PyObject * y = PySequence_GetItem(o, 1);
    v.x = PyFloat_AsDouble(x);
    v.y = PyFloat_AsDouble(y);

    Py_DECREF(x);
    Py_DECREF(y);

    return v;
}

static Vector vector_from_attribute(PyObject * o, char * name)
{
    PyObject * o2 = PyDict_GetItemString(o, name);
    Vector result = vector_from_pyobject(o2);
    return result;
}

static void pedestrian_from_pyobject(PyObject * o, Pedestrian * a)
{
	Vector null_vector ={0.0,0.0};

    a->radius                   = double_from_attribute(o, "radius");
    a->time                     = double_from_attribute(o, "time");
    a->initial_desired_velocity = double_from_attribute(o, "initial_desired_velocity");
    a->relax_time               = double_from_attribute(o, "relax_time");
    a->interaction_constant     = double_from_attribute(o, "interaction_constant");
    a->interaction_distance		= double_from_attribute(o, "interaction_distance");
    a->p_type					= double_from_attribute(o, "p_type");

    memset(&a->flowline, 0, 5*sizeof(int));

    a->position         = vector_from_attribute(o, "position");
    a->free_velocity 	= null_vector;
    a->target           = vector_from_attribute(o, "target");
    a->velocity         = vector_from_attribute(o, "velocity");
    a->acceleration     = vector_from_attribute(o, "acceleration");
}

static PyObject * add_pedestrian(PyObject * self, PyObject * args)
{
    PyObject * p_pedestrian;
    int i = a_count;

    PyArg_ParseTuple(args, "O:add_pedestrians", &p_pedestrian);

	update_total_count(a_count+1);
	pedestrian_from_pyobject(p_pedestrian, &pedestrians[i]);

    Py_RETURN_NONE;
}

static PyObject * update_pedestrians(PyObject * self, PyObject * args)
{
	int i;
	for(i = 0; i < a_count; i++) {
		// compute desired force for each pedestrian
		calculate_desired_acceleration(&pedestrians[i]);

		// compute interaction force for pedestrian i
		calculate_pedestrian_repulsion(i);
	}

	//update position and check escape or not
	for(i = 0; i < a_count; i++) {
	   update_position(&pedestrians[i]);
	}

	check_escapes();
	Py_RETURN_NONE;
}

static void update_position(Pedestrian * a)
{
	Vector delta_p = vector_add(
				vector_mul(a->velocity, timestep),
				vector_mul(a->acceleration, 0.5 * pow(timestep, 2)));

	    vector_iadd(&a->position, &delta_p);
		a->velocity = vector_add(a->velocity,
				vector_mul(a->acceleration, timestep));
	    a->time += timestep;

	    check_flowlines(a);
}

static void check_flowlines(Pedestrian * a)
{
    int i;
    for(i=0; i<fline_c;i++) {
        if(!a->flowline[i] && vector_projection_distance(//only check when a->flowline[i]==0
                    flowlines[i].start, flowlines[i].end, a->position) < a->radius) {
            new_flow_c[i] += 1;
            a->flowline[i] = 1;
        }
    }
}

static PyObject * flow_count(PyObject * self, PyObject * args)
{
	PyObject * f_c;
    Py_ssize_t i;

    PyArg_ParseTuple(args, "i:flow_count", &i);
    if(i > fline_c) Py_RETURN_NONE;

	f_c = PyFloat_FromDouble(new_flow_c[i]);
	new_flow_c[i] = 0;
	return f_c;
}

static void calculate_desired_acceleration(Pedestrian * a){
	    Vector desired_direction = {0.0, 0.0};

	   	desired_direction = vector_sub(a->target, a->position);
	    vector_unitise(&desired_direction);//compute unit vector of desired direction

	    a->free_velocity = vector_mul(desired_direction, a->initial_desired_velocity);

	    a->acceleration = a->free_velocity;
	    vector_isub(&a->acceleration, &a->velocity);
	    vector_imul(&a->acceleration, 1.0/a->relax_time);
}

static void calculate_pedestrian_repulsion(int index)
{
	int j;
	int flag = 0;
	Vector total_repulsion;
	Vector temp_repulsion;
	for(j = 0; j < a_count; j++) {
	        if(index == j) continue;
	        //check whether pedestrian j is front of pedestrian index
	        flag = is_front_of(pedestrians[index],pedestrians[j]);
	        if( flag ==1){
	        	temp_repulsion = calculate_repulsion_vector(pedestrians[index],pedestrians[j]);
	        	vector_iadd(&total_repulsion, &temp_repulsion);
	        }
	}
	vector_imul(&total_repulsion,pedestrians[index].interaction_constant);
	vector_isub(&pedestrians[index].acceleration, &total_repulsion);
}

static void check_escapes()
{
	int i, j;
		for(i = 0, j = 0; i < a_count; i++) {
			if(!is_escaped(&pedestrians[i])) {
				pedestrians[j++] = pedestrians[i];
			}
		}
		if(i!=j) {
			update_total_count(a_count - (i-j));
			escaped_count += i-j;
		}
}

static int is_escaped(Pedestrian * a)
{
	double current_pedestrian_x = a->position.x;
	double target =  a->target.x;
	double distance = sqrt((current_pedestrian_x - target)*(current_pedestrian_x - target));
	if (distance <= a->radius*2) return 1;
    return 0;
}

static int is_front_of(Pedestrian a, Pedestrian b)
{
	Vector from_a_to_b;
	Vector desired_direction;

	int flag;
	from_a_to_b = vector_sub(b.position,a.position);
	flag = vector_is_same_direction(a.velocity,from_a_to_b);
	if (flag ==0) {
		return flag;
	}
	if( flag == 1){ //check with his target direction
	 	desired_direction = vector_sub(a.target, a.position);
		vector_unitise(&desired_direction);
		return vector_is_same_direction(desired_direction,from_a_to_b);
	}
}

//this method is to calculate the repulsion force created by Pedestrian b on Pedestrian a
static Vector calculate_repulsion_vector(Pedestrian a, Pedestrian b)
{
	Vector from_a_to_b;
	double distance;
	double radius_sum;

	from_a_to_b= vector_sub(b.position,a.position);
	distance   = vector_length(from_a_to_b);
	vector_unitise(&from_a_to_b);

	radius_sum = a.radius + b.radius;
	distance = (-1) *(distance-radius_sum);
	vector_imul(&from_a_to_b, exp(distance/a.interaction_distance));

	return from_a_to_b;
}

static PyObject * a_property(PyObject * self, PyObject * args)
{

    Py_ssize_t i;
	char * property;
    PyArg_ParseTuple(args, "is:a_property", &i, &property);

	if(i > a_count) {
		PyErr_SetString(PyExc_KeyError, NULL);
		return NULL;
	}

	if(strcmp(property, "position") == 0) {
		return Py_BuildValue("dd",pedestrians[i].position.x, pedestrians[i].position.y);
	} else if(strcmp(property, "radius") == 0) {
		return PyFloat_FromDouble(pedestrians[i].radius);
	} else if(strcmp(property, "velocity") == 0) {
		return PyFloat_FromDouble(vector_length(pedestrians[i].velocity));
	} else if (strcmp(property, "p_type") == 0){
		return PyFloat_FromDouble(pedestrians[i].p_type);
	}else if(strcmp(property, "target") == 0) {
		return Py_BuildValue("dd", 
				pedestrians[i].target.x, pedestrians[i].target.y);
	}

	PyErr_SetString(PyExc_AttributeError, property);
	return NULL;
}

static PyObject * set_parameters(PyObject * self, PyObject * args)
{
	PyObject * o, *p_flowlines;
	PyArg_ParseTuple(args, "O:set_parameters", &o);

	timestep    = double_from_attribute(o, "timestep");

	p_flowlines  = PyDict_GetItemString(o, "flowrate_lines");

	//create flow line to measure escape number
	fline_c = PyList_Size(p_flowlines);
	flowlines   = PyMem_Realloc(flowlines, fline_c * sizeof(Wall));
	init_walls(p_flowlines, flowlines, fline_c);

	//create flow line to measure flow rate
	new_flow_c  = PyMem_Realloc(new_flow_c, fline_c * sizeof(Py_ssize_t));
	memset(new_flow_c, 0, fline_c * sizeof(Py_ssize_t));


	update_total_count(0);

	Py_RETURN_NONE;
}

static Wall wall_from_pyobject(PyObject *o)
{
    Wall w;
    w.start.x = PyFloat_AsDouble(PyTuple_GetItem(o, 0));
    w.start.y = PyFloat_AsDouble(PyTuple_GetItem(o, 1));
    w.end.x   = PyFloat_AsDouble(PyTuple_GetItem(o, 2));
    w.end.y   = PyFloat_AsDouble(PyTuple_GetItem(o, 3));
    w.length  = vector_length(vector_sub(w.end, w.start));

    return w;
}

static void init_walls(PyObject * p_walls, Wall * walls_p, Py_ssize_t w_count)
{
    int i;
    for(i = 0; i < w_count; i++) {
        PyObject * p_w   = PyList_GetItem(p_walls, i);
        Wall w = wall_from_pyobject(p_w);
        walls_p[i] = w;
    }
}

static PyObject * reset_model(PyObject* self)
{
		int i;
	    a_count     = -1; //reset total pedestrian number
	    escaped_count = 0; //reser escaped pedestrian number
	    pedestrians = NULL;
		update_total_count(0);

		//reset flow rate observation
		if (new_flow_c !=0){
			for(i=0;i< fline_c;i++){
				new_flow_c[i] = 0;
			}
		}

		Py_RETURN_NONE;
}

static PyMethodDef ForceModelMethods[] = {
    {"add_pedestrian", add_pedestrian, METH_VARARGS, 
        "Add an pedestrian to the list"},
	{"set_parameters",set_parameters,METH_VARARGS,
		"Set simulation parameters"},
    {"a_property", a_property, METH_VARARGS, 
        "Get a property for an pedestrian"},
	{"get_total_count",(PyCFunction)get_total_count,METH_NOARGS,
		"Get total population number"},
	{"update_pedestrians",update_pedestrians,METH_VARARGS,
		"Calculate the acceleration of an pedestrian"},
	{"flow_count", flow_count, METH_VARARGS,
		"Get number of pedestrians that have passed the flow line"},
	{"get_escaped_count",(PyCFunction)get_escaped_count,METH_NOARGS,
		"Get total escaped number"},
	{"reset_model",(PyCFunction)reset_model,METH_NOARGS,
				"Reset model for parameters and pedestrians"},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef forceCalculationmodule = {
		PyModuleDef_HEAD_INIT,
		"nomadmodel",
		NULL,
		-1,
		ForceModelMethods
	};

PyMODINIT_FUNC PyInit_nomadmodel(void)
{
	PyObject * m;
	m = PyModule_Create(&forceCalculationmodule);

    a_count     = -1; //reset total pedestrian number
	escaped_count = 0; //reset escaped pedestrian number
	pedestrians = NULL;
	timestep    = 0;//reset timestep
	update_total_count(0);

    new_flow_c  = 0;

    return m;
}
