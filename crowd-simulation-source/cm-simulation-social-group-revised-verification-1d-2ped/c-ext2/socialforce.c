#include "socialforce.h"

static Pedestrian * group_pedestrians;

static Py_ssize_t group_population_count;

static Py_ssize_t w_count;

static double timestep;

static double group_centre_of_mass;

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

static void pedestrian_from_pyobject(PyObject * o, Pedestrian * a)
{
	int i;
    a->radius                   = double_from_attribute(o, "radius");
    a->time                     = double_from_attribute(o, "time");

    a->pedestrian_id			= double_from_attribute(o,"pedestrian_id");

    a->force_unit               = double_from_attribute(o, "force_unit");
    a->interaction_range		= double_from_attribute(o, "interaction_range");

    a->att_unit					= double_from_attribute(o,"attraction_strength");
    a->att_range				= double_from_attribute(o,"attraction_range");

    a->position         		= double_from_attribute(o, "position");
    a->velocity         		= double_from_attribute(o, "velocity");
    a->acceleration     		= double_from_attribute(o, "acceleration");

    a->velocity_temp			= 0.0;
    a->position_temp			= 0.0;

    a->previous_velocity 		= 0.0;
    a->previous_position		= 0.0;

    //initial level of Runge Kutta method, 0 element is for initial
    for(i=0; i <4; i++){
    	a->acceleration_rk[i] = 0.0;
    	a->velocity_rk[i] = 0.0;
    	a->position_rk[i] = 0.0;
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
	group_centre_of_mass=0;
	
	for(i = 0; i < group_population_count; i++)
		group_centre_of_mass+= group_pedestrians[i].position;

	group_centre_of_mass/=group_population_count;

}

static void rk_appropximate_level(int level_k){

	int i;
	if(level_k==1){ //compute at level 1
		for(i = 0; i < group_population_count; i++) {
			//reset acceleration at each  level 1 before computing it
			group_pedestrians[i].acceleration_rk[0] =  0.0;
			group_pedestrians[i].position_temp = group_pedestrians[i].position;

			//collect previous position and velocity
			group_pedestrians[i].previous_velocity = group_pedestrians[i].velocity;
			group_pedestrians[i].previous_position = group_pedestrians[i].position;

		}

		for(i = 0; i < group_population_count; i++) {
			// compute interaction force for pedestrian i at level 1
			calculate_pedestrian_repulsion(&group_pedestrians[i],i,0);
			// compute attraction force for pedestrian i at level 1
			calculate_group_force(&group_pedestrians[i],i,0);
		}

		for(i = 0; i < group_population_count; i++) {
			group_pedestrians[i].velocity_rk[0] = group_pedestrians[i].acceleration_rk[0] * timestep;
			group_pedestrians[i].position_rk[0] = group_pedestrians[i].velocity * timestep;
		}
	}
	else if(level_k==2){ //compute at level 2
		for(i = 0; i < group_population_count; i++) {
			//reset acceleration at each  level k before computing it
			group_pedestrians[i].acceleration_rk[1] =  0.0;
			group_pedestrians[i].position_temp = group_pedestrians[i].position +  (group_pedestrians[i].position_rk[0] * 0.5);
		}

		for(i = 0; i < group_population_count; i++) {
			// compute interaction force for pedestrian i at level 2
			calculate_pedestrian_repulsion(&group_pedestrians[i],i,1);
			// compute attraction force for pedestrian i at level 2
			calculate_group_force(&group_pedestrians[i],i,1);
		}

		for(i = 0; i < group_population_count; i++) {
			group_pedestrians[i].velocity_rk[1] = group_pedestrians[i].acceleration_rk[1] * timestep;
			group_pedestrians[i].position_rk[1] = (group_pedestrians[i].velocity + (group_pedestrians[i].velocity_rk[0] * 0.5)) * timestep;
		}
	}
	else if(level_k==3){
		for(i = 0; i < group_population_count; i++) {
			//reset acceleration at each  level k before computing it
			group_pedestrians[i].acceleration_rk[2] = 0.0;
			group_pedestrians[i].position_temp = group_pedestrians[i].position + (group_pedestrians[i].position_rk[1] * 0.5);
		}

		for(i = 0; i < group_population_count; i++) {
			// compute interaction force for pedestrian i at level 3
			calculate_pedestrian_repulsion(&group_pedestrians[i],i,2);
			// compute attraction force for pedestrian i at level 3
			calculate_group_force(&group_pedestrians[i],i,2);
		}
		for(i = 0; i < group_population_count; i++) {
			group_pedestrians[i].velocity_rk[2] = group_pedestrians[i].acceleration_rk[2] * timestep;
			group_pedestrians[i].position_rk[2] = (group_pedestrians[i].velocity + (group_pedestrians[i].velocity_rk[1] * 0.5)) * timestep;
		}
	}
	else if(level_k==4){
		for(i = 0; i < group_population_count; i++) {
			//reset acceleration at each  level k before computing it
			group_pedestrians[i].acceleration_rk[3] = 0.0;
			group_pedestrians[i].position_temp = group_pedestrians[i].position + group_pedestrians[i].position_rk[2];

		}

		for(i = 0; i < group_population_count; i++) {
			// compute interaction force for pedestrian i at level 4
			calculate_pedestrian_repulsion(&group_pedestrians[i],i,3);
			// compute attraction force for pedestrian i at level 4
			calculate_group_force(&group_pedestrians[i],i,3);
		}
		for(i = 0; i < group_population_count; i++) {
			group_pedestrians[i].velocity_rk[3] = group_pedestrians[i].acceleration_rk[3] * timestep;
			group_pedestrians[i].position_rk[3] = (group_pedestrians[i].velocity + group_pedestrians[i].velocity_rk[2]) * timestep;
		}
	}

	return;
}

static PyObject * update_pedestrians(PyObject * self, PyObject * args)
{
	int i;
	
	identify_group_centre_of_mass();

	//compute RK level1
	rk_appropximate_level(1);

	//compute RK level2
	rk_appropximate_level(2);

	//compute RK level3
	rk_appropximate_level(3);

	//compute RK level4
	rk_appropximate_level(4);

	//update position for in-group pedestrians
	for(i = 0; i < group_population_count; i++) {
	   update_position(&group_pedestrians[i]);
	}
	
	Py_RETURN_NONE;
}

static void update_position(Pedestrian * a)
{

	double delta_v, delta_v_temp, delta_p, delta_p_temp;

	//update position
	delta_p = a->position_rk[0] + (a->position_rk[1] *2);
	delta_p_temp =(a->position_rk[2] * 2) + a->position_rk[3];
	delta_p += delta_p_temp;
	delta_p*=(1/6.0);
	a->position = a->position + delta_p;


	//update velocity
	delta_v = a->velocity_rk[0] + (a->velocity_rk[1] * 2);
	delta_v_temp = (a->velocity_rk[2] * 2) + a->velocity_rk[3];
	delta_v += delta_v_temp;
	delta_v*= (1/6.0);
	a->velocity = a->velocity + delta_v;

	a->time += timestep;

}

static void calculate_pedestrian_repulsion(Pedestrian * a,int index,int level_rk)
{
	int j;
	double repulsion;
	double *current_value;
	//compute repulsion force for group pedestrian
	for(j = 0; j < group_population_count; j++) {
	    if(index == j) continue;
	        
		//we compute the force between this two pedestrians
	    repulsion = calculate_i_repulsion_vector(a,group_pedestrians[j],level_rk);
		current_value =   &a->acceleration_rk[level_rk];
		*current_value += repulsion;

	}
}

//this method is to calculate the repulsion force created by Pedestrian b on Pedestrian * a
static double calculate_i_repulsion_vector(Pedestrian *a, Pedestrian b,int level_rk)
{
	double radius_sum = a->radius + b.radius;
	double distance   = fabs(a->position_temp - b.position_temp);
	
	double from_b =  a->force_unit * exp((radius_sum-distance)/a->interaction_range);
	if (b.position_temp > a->position_temp){
		return (-1) * from_b;
	} else {
		return from_b;
	}
}

static void  calculate_group_force(Pedestrian *a,int index,int level_rk)
{
	int j;
	double attraction;
	double *current_value;
	//compute attraction force for group pedestrian
	for(j = 0; j < group_population_count; j++) {
		if(index == j) continue;
		
		//we compute the attraction force between this two pedestrians
		attraction = calculate_i_attraction_vector(a,group_pedestrians[j],level_rk);
		current_value = &a->acceleration_rk[level_rk];
		*current_value += attraction ;
	}
}

//this method is to calculate the attraction force created by Pedestrian a on Pedestrian * a
static double calculate_i_attraction_vector(Pedestrian *a, Pedestrian b,int level_rk)
{
	double radius_sum = a->radius + b.radius;
	double distance   = fabs(b.position_temp - a->position_temp);

	double from_a = a->att_unit * exp((radius_sum-distance)/a->att_range);
	if(b.position_temp > a->position_temp){
		return from_a;
	}else {
		return (-1)*from_a;
	}

}

//this method is to retrieve information of group member a
static PyObject * group_pedestrian_a_property(PyObject * self, PyObject * args)
{

	double distance;
    Py_ssize_t i;
	char * property;
    PyArg_ParseTuple(args, "is:group_pedestrian_a_property", &i, &property);

	if(i > group_population_count) {
		PyErr_SetString(PyExc_KeyError, NULL);
		return NULL;
	}

	if(strcmp(property, "position") == 0) {
		return PyFloat_FromDouble(group_pedestrians[i].position);
	} else if(strcmp(property, "radius") == 0) {
		return PyFloat_FromDouble(group_pedestrians[i].radius);
	}  else if(strcmp(property, "velocity") ==0){
		return PyFloat_FromDouble(group_pedestrians[i].velocity);
	} else if(strcmp(property, "distance") ==0){
		distance= fabs(group_pedestrians[0].position - group_pedestrians[1].position);
		return PyFloat_FromDouble(distance);
	} else if(strcmp(property, "velocity_rk") == 0){
		return Py_BuildValue("ddddd", group_pedestrians[i].previous_velocity,
				group_pedestrians[i].velocity_rk[0], group_pedestrians[i].velocity_rk[1],group_pedestrians[i].velocity_rk[2],group_pedestrians[i].velocity_rk[3]);
	} else if(strcmp(property, "position_rk") == 0){
		return Py_BuildValue("ddddd", group_pedestrians[i].previous_position,
				group_pedestrians[i].position_rk[0], group_pedestrians[i].position_rk[1],group_pedestrians[i].position_rk[2],group_pedestrians[i].position_rk[3]);
	} else if(strcmp(property, "id") ==0){
		return PyFloat_FromDouble(group_pedestrians[i].pedestrian_id);
	}

	PyErr_SetString(PyExc_AttributeError, property);
	return NULL;
}

static PyObject * get_group_centre_of_mass(PyObject * self)
{
	return PyFloat_FromDouble(group_centre_of_mass); 
}

static PyObject * get_group_cohesion_degree(PyObject * self)
{
	double group_cohesion_degree=0;
	int j;
	double distance;
	//compute group cohesion degree for group pedestrian
	for(j = 0; j < group_population_count; j++)
	{
		distance = fabs(group_pedestrians[j].position - group_centre_of_mass);
		group_cohesion_degree += distance;
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

	group_centre_of_mass =0;
	
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

	group_centre_of_mass =0;
	
    group_pedestrians=NULL;
	
    timestep    = 0; //reset timestep
	
	update_total_group_member_count(0);
	
    return m;
}
