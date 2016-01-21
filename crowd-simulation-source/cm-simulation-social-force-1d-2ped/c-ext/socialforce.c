#include "socialforce.h"

static Pedestrian * pedestrians;
static Py_ssize_t population_count;
static Py_ssize_t escaped_count;

static double timestep;

static void update_total_count(Py_ssize_t count)
{
	if(count == population_count) return;
	population_count = count;
	pedestrians = PyMem_Realloc(pedestrians, population_count * sizeof(Pedestrian));
}

static PyObject* get_population_size(PyObject* self)
{
	return PyFloat_FromDouble(population_count);
}

static PyObject* get_escaped_num(PyObject* self)
{
	return PyFloat_FromDouble(escaped_count);
}

static double double_from_attribute(PyObject * o, char * name)
{
    PyObject * o2 = PyDict_GetItemString(o, name);
    double result = PyFloat_AsDouble(o2);
    return result;
}

static void pedestrian_from_pyobject(PyObject * o, Pedestrian * a)
{
    a->time                     = double_from_attribute(o, "time");
    a->initial_desired_velocity = double_from_attribute(o, "initial_desired_velocity");
    a->force_unit               = double_from_attribute(o, "force_unit");
    a->pedestrian_id			= double_from_attribute(o,"pedestrian_id");

    a->position         			= double_from_attribute(o, "position");
    a->target           			= double_from_attribute(o, "target");
    a->velocity         			= double_from_attribute(o, "velocity");
    a->desired_force_tracking 		= double_from_attribute(o, "desired_force_tracking");
    a->interaction_force_tracking 	= double_from_attribute(o, "interaction_force_tracking");

    a->initial_position= double_from_attribute(o, "initial_position");
    a->distance_travelled = double_from_attribute(o, "distance_travelled");
    a->is_not_moving = double_from_attribute(o, "is_not_moving");
}

static PyObject * add_pedestrian(PyObject * self, PyObject * args)
{
    PyObject * p_pedestrian;
    int i = population_count;

    PyArg_ParseTuple(args, "O:add_pedestrians", &p_pedestrian);

	update_total_count(population_count+1);
	pedestrian_from_pyobject(p_pedestrian, &pedestrians[i]);

    Py_RETURN_NONE;
}

static PyObject * update_pedestrians(PyObject * self, PyObject * args)
{
	int i;

	for(i = 0; i < population_count; i++) {
		calculate_desired_acceleration(&pedestrians[i]);
		calculate_pedestrian_repulsion(i);

	}
	//e = 2.71828183

	//update position and check escape or not
	for(i = 0; i < population_count; i++) {
	   update_position(&pedestrians[i]);
	}

	check_escapes();
	Py_RETURN_NONE;
}

static void update_position(Pedestrian * a)
{
	int _int_speed ;
	double delta_p = a->velocity * timestep;

	a->position = a->position + delta_p;
	a->time += timestep;

	_int_speed = (int)a->velocity;
	if(_int_speed == 0){
		a->is_not_moving = 1;
	} else{
		a->is_not_moving = 0;
	}

	a->distance_travelled = fabs(a->position-a->initial_position);
}

static void calculate_desired_acceleration(Pedestrian * a)
{	
		if (a->position > a->target){
			a->velocity = (-1 )* a->initial_desired_velocity * a->position;
		} else {
			a->velocity = a->initial_desired_velocity * a->position * (-1); //because position less than 0
		}
	    a->desired_force_tracking  = a->velocity;
}

static void calculate_pedestrian_repulsion(int index)
{
	int j;

	double repulsion=0.0;
	double distance_from_a_b;
	
	//reset interaction force
	pedestrians[index].interaction_force_tracking= 0.0;

	for(j = 0; j < population_count; j++) {
	        if(index == j) continue;
	        	distance_from_a_b = fabs(pedestrians[j].position - pedestrians[index].position);

	        	repulsion = pedestrians[index].force_unit * exp((-1) * distance_from_a_b);

	        	if(pedestrians[j].position > pedestrians[index].position ){
	        		repulsion *= -1;
	        	}
	        pedestrians[index].velocity +=repulsion;
	       	pedestrians[index].interaction_force_tracking += repulsion;

	}
}

static void check_escapes()
{
	int i, j;
		for(i = 0, j = 0; i < population_count; i++) {
			if(!is_escaped(&pedestrians[i])) {
				pedestrians[j++] = pedestrians[i];
			}
		}
		if(i!=j){
			update_total_count(population_count - (i-j));
			escaped_count += i-j;
		}
}

static int is_escaped(Pedestrian * a)
{
	double distance = fabs(a->position - a->target);
	if (distance ==0 || distance<=0.2) return 1;
	return 0;
}

static PyObject * a_property(PyObject * self, PyObject * args)
{

    Py_ssize_t i;
	char * property;
    PyArg_ParseTuple(args, "is:a_property", &i, &property);

	if(i > population_count) {
		PyErr_SetString(PyExc_KeyError, NULL);
		return NULL;
	}

	if(strcmp(property, "position") == 0) {
		return PyFloat_FromDouble(pedestrians[i].position);
	} else if(strcmp(property, "initial_position") == 0) {
		return PyFloat_FromDouble(pedestrians[i].initial_position);
	}else if(strcmp(property, "velocity") == 0) {
		return PyFloat_FromDouble(pedestrians[i].velocity);
	} else if(strcmp(property, "id") ==0){
		return PyFloat_FromDouble(pedestrians[i].pedestrian_id);

	} else if(strcmp(property, "initial_desired_velocity") == 0) {
		return PyFloat_FromDouble(pedestrians[i].initial_desired_velocity);
	}else if(strcmp(property,"desired_force_tracking") == 0){
		return PyFloat_FromDouble(pedestrians[i].desired_force_tracking);

	}else if(strcmp(property, "force_unit") == 0) {
		return PyFloat_FromDouble(pedestrians[i].force_unit);
	} else if(strcmp(property,"interaction_force_tracking") == 0){
		return PyFloat_FromDouble(pedestrians[i].interaction_force_tracking);

	}else if(strcmp(property, "time_travelled") == 0) {
			return PyFloat_FromDouble(pedestrians[i].time);
	} else if(strcmp(property, "distance_travelled") == 0) {
		return PyFloat_FromDouble(pedestrians[i].distance_travelled);
	} else if(strcmp(property, "is_not_moved") == 0) {
		return PyFloat_FromDouble(pedestrians[i].is_not_moving);
	}

	PyErr_SetString(PyExc_AttributeError, property);
	return NULL;
}

static PyObject * is_bottle_neck(PyObject * self)
{
	int i;
	int not_moving=0;
	for(i = 0; i < population_count; i++) {
		if (pedestrians[i].is_not_moving== 1){
			not_moving++;
		}
	}

	if(not_moving == population_count) {
		 return Py_BuildValue("i",1);
	} else{
		 return Py_BuildValue("i",0);
	}

}
static PyObject * check_escaped(PyObject * self, PyObject * args)
{
	  double ped_id;
	  int index;
	  PyArg_ParseTuple(args, "d:check_escaped", &ped_id);

	  for(index = 0; index < population_count; index++) {
		  if(pedestrians[index].pedestrian_id == ped_id){
			  return Py_BuildValue("i",0);
		  }
	  }

	  return Py_BuildValue("i",1);
}

static PyObject * set_parameters(PyObject * self, PyObject * args)
{
	PyObject * o;
	PyArg_ParseTuple(args, "O:set_parameters", &o);
	timestep    = double_from_attribute(o, "timestep");
	update_total_count(0);

	Py_RETURN_NONE;
}


static PyObject * reset_model(PyObject* self)
{
	    population_count     = -1; //reset total pedestrian number
	    escaped_count = 0; //reset escaped pedestrian number

	    pedestrians = NULL;
		update_total_count(0);

		Py_RETURN_NONE;
}

static PyMethodDef ForceModelMethods[] = {
    {"add_pedestrian", add_pedestrian, METH_VARARGS, 
        "Add an pedestrian to the list"},
	{"set_parameters",set_parameters,METH_VARARGS,
		"Set simulation parameters"},
    {"a_property", a_property, METH_VARARGS, 
        "Get a property for an pedestrian"},
	{"get_population_size",(PyCFunction)get_population_size,METH_NOARGS,
		"Get total population number"},
	{"update_pedestrians",update_pedestrians,METH_VARARGS,
		"Calculate the acceleration of an pedestrian"},
	{"get_escaped_num",(PyCFunction)get_escaped_num,METH_NOARGS,
		"Get total escaped number"},
	{"is_bottle_neck",(PyCFunction)is_bottle_neck,METH_NOARGS,
		"Check bottleneck"},
	{"reset_model",(PyCFunction)reset_model,METH_NOARGS,
		"Reset model for parameters and pedestrians"},
	{"check_escaped", check_escaped, METH_VARARGS,
		"Check a pedestrian escaped by ped_id"},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef forceCalculationmodule = {
		PyModuleDef_HEAD_INIT,
		"socialforce",
		NULL,
		-1,
		ForceModelMethods
	};

PyMODINIT_FUNC PyInit_socialforce(void)
{
	PyObject * m;
	m = PyModule_Create(&forceCalculationmodule);

    population_count     = -1; //reset total pedestrian number
    escaped_count = 0; //reset escaped pedestrian number

    pedestrians = NULL;
    timestep    = 0; //reset timestep

	update_total_count(0);

    return m;
}
