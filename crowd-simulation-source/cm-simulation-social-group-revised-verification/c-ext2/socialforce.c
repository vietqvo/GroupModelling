#include "socialforce.h"

static Pedestrian * group_pedestrians;

static Py_ssize_t group_population_count;

static Py_ssize_t w_count;

static double timestep;

static Vector group_centre_of_mass;


static void update_total_group_member_count(Py_ssize_t count)
{
	if(count == group_population_count) return;
	group_population_count = count;
	group_pedestrians = PyMem_Realloc(group_pedestrians, group_population_count * sizeof(Pedestrian));
}

static PyObject* get_population_size(PyObject* self)
{
	return PyFloat_FromDouble(group_population_count);
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
	int i;
    a->radius                   = double_from_attribute(o, "radius");
    a->time                     = double_from_attribute(o, "time");

    a->force_unit               = double_from_attribute(o, "force_unit");
    a->interaction_range		= double_from_attribute(o, "interaction_range");

    a->att_unit					= double_from_attribute(o, "attraction_strength");
    a->att_range				= double_from_attribute(o, "attraction_range");

    a->p_type					= double_from_attribute(o, "p_type");
    a->pedestrian_id			= double_from_attribute(o, "pedestrian_id");

    a->position         		= vector_from_attribute(o, "position");
    a->initial_position 		= vector_from_attribute(o, "initial_position");
    a->velocity         		= vector_from_attribute(o, "velocity");
    a->acceleration     		= vector_from_attribute(o, "acceleration");

    a->position_temp			= vector_mul(a->position,0.0);

    //initial level of Runge Kutta method, 0 element is for initial
    for(i=0; i <5; i++){
    	a->acceleration_rk [i] = vector_mul(a->acceleration,0.0);
    	a->position_rk[i] = vector_mul(a->position,0.0);
    }
}

static PyObject * add_group_pedestrian(PyObject * self, PyObject * args)
{
    PyObject * p_pedestrian;
    int i = group_population_count;

    PyArg_ParseTuple(args, "O:add_group_pedestrian", &p_pedestrian);

	update_total_group_member_count(group_population_count+1);
	pedestrian_from_pyobject(p_pedestrian, &group_pedestrians[i]);

    Py_RETURN_NONE;
}


static void identify_group_centre_of_mass()
{
	int i;
	group_centre_of_mass.x=0;
	group_centre_of_mass.y=0;

	for(i = 0; i < group_population_count; i++)
		vector_iadd(&group_centre_of_mass,&group_pedestrians[i].position);

	vector_unitise_c(&group_centre_of_mass,group_population_count);

}

static void rk_appropximate_level(int level_k){

	int i;
	if(level_k==0){ //compute at level 1
		for(i = 0; i < group_population_count; i++) {
			//reset acceleration at each  level 1 before computing it
			vector_imul(&group_pedestrians[i].acceleration_rk[0], 0.0);
			group_pedestrians[i].position_temp = group_pedestrians[i].position;
		}

		for(i = 0; i < group_population_count; i++) {
			// compute interaction attraction force for pedestrian i at level 1
			calculate_pedestrian_repulsion_attraction(&group_pedestrians[i],i,0);
		}

		for(i = 0; i < group_population_count; i++) {
			group_pedestrians[i].position_rk[0] = vector_mul(group_pedestrians[i].acceleration_rk[0],timestep);
		}
	}
	else if(level_k==1){ //compute at level 2
		for(i = 0; i < group_population_count; i++) {
			//reset acceleration at each  level k before computing it
			vector_imul(&group_pedestrians[i].acceleration_rk[1], 0.0);
			group_pedestrians[i].position_temp = vector_add(group_pedestrians[i].position, vector_mul(group_pedestrians[i].position_rk[0], 0.5));
		}

		for(i = 0; i < group_population_count; i++) {
			// compute interaction force for pedestrian i at level 2
			calculate_pedestrian_repulsion_attraction(&group_pedestrians[i],i,1);
		}

		for(i = 0; i < group_population_count; i++) {
			group_pedestrians[i].position_rk[1] = vector_mul(group_pedestrians[i].acceleration_rk[1],timestep);
		}
	}
	else if(level_k==2){ //compute at level 3
		for(i = 0; i < group_population_count; i++) {
			//reset acceleration at each  level k before computing it
			vector_imul(&group_pedestrians[i].acceleration_rk[2], 0.0);
			group_pedestrians[i].position_temp = vector_add(group_pedestrians[i].position, vector_mul(group_pedestrians[i].position_rk[1], 0.5));
		}

		for(i = 0; i < group_population_count; i++) {
			// compute interaction force for pedestrian i at level 3
			calculate_pedestrian_repulsion_attraction(&group_pedestrians[i],i,2);
		}
		
		for(i = 0; i < group_population_count; i++) {
			group_pedestrians[i].position_rk[2] = vector_mul(group_pedestrians[i].acceleration_rk[2],timestep);
		}
	}
	else if(level_k==3){ //compute at level 4
		for(i = 0; i < group_population_count; i++) {
			//reset acceleration at each  level k before computing it
			vector_imul(&group_pedestrians[i].acceleration_rk[3], 0.0);
			group_pedestrians[i].position_temp = vector_add(group_pedestrians[i].position, group_pedestrians[i].position_rk[2]);

		}

		for(i = 0; i < group_population_count; i++) {
			// compute interaction force for pedestrian i at level 4
			calculate_pedestrian_repulsion_attraction(&group_pedestrians[i],i,3);
		}

		for(i = 0; i < group_population_count; i++) {
			group_pedestrians[i].position_rk[3] = vector_mul(group_pedestrians[i].acceleration_rk[3],timestep);
		}
	}

	return;
}

static PyObject * update_pedestrians(PyObject * self, PyObject * args)
{
	int i;
	
	identify_group_centre_of_mass();

	//compute RK level1
	rk_appropximate_level(0);

	//compute RK level2
	rk_appropximate_level(1);

	//compute RK level3
	rk_appropximate_level(2);

	//compute RK level4
	rk_appropximate_level(3);

	//update position for in-group pedestrians
	for(i = 0; i < group_population_count; i++) {
	   update_position(&group_pedestrians[i]);
	}
	
	Py_RETURN_NONE;
}

static void update_position(Pedestrian * a)
{

	Vector delta_p, delta_p_temp;

	//update position
	delta_p = vector_add(a->position_rk[0],vector_mul(a->position_rk[1],2));
	delta_p_temp = vector_add(vector_mul(a->position_rk[2],2),a->position_rk[3]);
	vector_iadd(&delta_p,&delta_p_temp);
	vector_imul(&delta_p,1/6.0);
	a->position = vector_add(a->position,delta_p);

	a->time += timestep;

}

static void calculate_pedestrian_repulsion_attraction(Pedestrian * a,int index,int level_rk)
{
	int j;
	double repulsion, attraction;
	Vector interaction;
	//compute repulsion force for group pedestrian
	for(j = 0; j < group_population_count; j++) {
	        if(index == j) continue;
	        
			//we compute the repulsion attraction force between this two pedestrians
	        repulsion = calculate_repulsion_magnitude(a,group_pedestrians[j]);
			
			//we compute the attraction force between this two pedestrians
			attraction = calculate_attraction_magnitude(a,group_pedestrians[j]);
			
			repulsion -=attraction;

			interaction = vector_sub(a->position_temp, group_pedestrians[j].position_temp);
			vector_unitise(&interaction);
			
			vector_imul(&interaction,repulsion);		
	        vector_iadd(&a->acceleration_rk[level_rk], &interaction);		
	}
}

//this method is to calculate the repulsion force created by Pedestrian b on Pedestrian * a
static double calculate_repulsion_magnitude(Pedestrian *a, Pedestrian b)
{
	double radius_sum = a->radius + b.radius;
	Vector from_b     = vector_sub(a->position_temp, b.position_temp);
	double distance   = fabs(vector_length(from_b) - radius_sum);
	
	double force_strength =  a->force_unit * exp((-distance)/a->interaction_range);
	
	return force_strength;

}

//this method is to calculate the attraction force created by Pedestrian b on Pedestrian * a
static double calculate_attraction_magnitude(Pedestrian *a, Pedestrian b)
{
	double radius_sum = a->radius + b.radius;
	Vector from_b     = vector_sub(a->position_temp, b.position_temp);
	double distance   = fabs(vector_length(from_b) - radius_sum);

	double force_strength =  a->att_unit * exp((-distance)/a->att_range);

	return force_strength;
}

//this method is to retrieve information of group member a
static PyObject * group_pedestrian_a_property(PyObject * self, PyObject * args)
{

    Py_ssize_t i;
	char * property;
    PyArg_ParseTuple(args, "is:group_pedestrian_a_property", &i, &property);

	if(i > group_population_count) {
		PyErr_SetString(PyExc_KeyError, NULL);
		return NULL;
	}

	if(strcmp(property, "position") == 0) {
		return Py_BuildValue("dd",
				group_pedestrians[i].position.x, group_pedestrians[i].position.y);
	} else if(strcmp(property, "initial_position") ==0) {
		return Py_BuildValue("dd",
				group_pedestrians[i].initial_position.x, group_pedestrians[i].initial_position.y);
	}else if(strcmp(property, "radius") == 0) {
		return PyFloat_FromDouble(group_pedestrians[i].radius);
	} else if (strcmp(property, "p_type") == 0){
		return PyFloat_FromDouble(group_pedestrians[i].p_type);
	} else if(strcmp(property, "id") ==0){
		return PyFloat_FromDouble(group_pedestrians[i].pedestrian_id);
	}

	PyErr_SetString(PyExc_AttributeError, property);
	return NULL;
}

static PyObject * get_group_centre_of_mass(PyObject * self)
{
	return Py_BuildValue("dd",
				group_centre_of_mass.x, group_centre_of_mass.y);
}

static PyObject * get_group_cohesion_degree(PyObject * self)
{
	double group_cohesion_degree=0;
	int j;
	Vector distance;
	//compute group cohesion degree for group pedestrian
	for(j = 0; j < group_population_count; j++)
	{
		distance = vector_sub(group_pedestrians[j].position,group_centre_of_mass);
		group_cohesion_degree += vector_length(distance);
	}
	
	return PyFloat_FromDouble(group_cohesion_degree/group_population_count);	
}


static PyObject * set_parameters(PyObject * self, PyObject * args)
{
	PyObject * o;
	PyArg_ParseTuple(args, "O:set_parameters", &o);

	timestep    = double_from_attribute(o, "timestep");

	update_total_group_member_count(0);
	
	Py_RETURN_NONE;
}

static PyObject * reset_model(PyObject* self)
{
	group_population_count     = -1; //reset total group member number

	group_centre_of_mass.x =0;
	group_centre_of_mass.y=0;
	
	group_pedestrians=NULL;
	
	update_total_group_member_count(0);

	Py_RETURN_NONE;
}

static PyMethodDef ForceModelMethods[] = {
    {"add_group_pedestrian", add_group_pedestrian, METH_VARARGS, 
        "Add an group member to the list"},
	{"set_parameters",set_parameters,METH_VARARGS,
		"Set simulation parameters"},
	{"group_pedestrian_a_property", group_pedestrian_a_property, METH_VARARGS, 
        "Get an property for group members"},	
	{"get_population_size",(PyCFunction)get_population_size,METH_NOARGS,
		"Get total population number"},
	{"update_pedestrians",update_pedestrians,METH_VARARGS,
		"Calculate the acceleration of an pedestrian"},
	{"reset_model",(PyCFunction)reset_model,METH_NOARGS,
		"Reset model for parameters and pedestrians"},
	{"get_group_centre_of_mass", (PyCFunction)get_group_centre_of_mass, METH_NOARGS,
		"Get group centre of mass over the time"},
	{"get_group_cohesion_degree", (PyCFunction)get_group_cohesion_degree, METH_NOARGS,
		"Get group cohesion degree over the time"},	
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef forceCalculationmodule = {
		PyModuleDef_HEAD_INIT,
		"socialforce2",
		NULL,
		-1,
		ForceModelMethods
	};

PyMODINIT_FUNC PyInit_socialforce2(void)
{
	PyObject * m;
	m = PyModule_Create(&forceCalculationmodule);

    group_population_count     = -1; //reset total group member number

	group_centre_of_mass.x =0;
	group_centre_of_mass.y=0;
	
    group_pedestrians=NULL;
	
    timestep    = 0; //reset timestep
	
	update_total_group_member_count(0);
	
    return m;
}
