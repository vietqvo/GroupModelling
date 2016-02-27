#include "socialforce.h"

static int group_num;
static int * group_population_count; //array to contain group size of each group --default = -1
static Pedestrian * group_pedestrians; //array to contain whole pedestrians of different groups 

static double timestep; //parameter to compute obstacle force

static void update_total_group_member_count(Py_ssize_t groupIndex, int count)//
{
//group index should run from 0
//default should set group_num = 0, and each group array size = 0

	int population_count=0;
	int i = 0, j=0;

	if (groupIndex < group_num && group_population_count !=NULL) {
		if(count == group_population_count[groupIndex]) return;
		else {
			group_population_count[groupIndex] = count;	
		}
	}
	else 
	{// when there is no group with this index, increase group num 
		group_num +=1;
		group_population_count = PyMem_Realloc(group_population_count, group_num * sizeof(int));
		//and allocate count for this group
		group_population_count[groupIndex] = count;	
	}

	//compute total population count, and corresponding counts for cd_inside group and between_groups
	for(i=0; i < group_num; i++) {
		population_count+= group_population_count[i];
	}		
	
	//re-allocate group_pedestrian number
	group_pedestrians = PyMem_Realloc(group_pedestrians, population_count * sizeof(Pedestrian));

}

static PyObject* get_population_size(PyObject* self)//
{
	int i;
	int population_count=0 ;
	for(i=0; i < group_num; i++) {
		population_count+= group_population_count[i];
	}
	return PyFloat_FromDouble(population_count);
}

static double double_from_attribute(PyObject * o, char * name)//
{
    PyObject * o2 = PyDict_GetItemString(o, name);
    double result = PyFloat_AsDouble(o2);
    return result;
}

static Vector vector_from_pyobject(PyObject * o)//
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

static Vector vector_from_attribute(PyObject * o, char * name)//
{
    PyObject * o2 = PyDict_GetItemString(o, name);
    Vector result = vector_from_pyobject(o2);
    return result;
}

static void pedestrian_from_pyobject(PyObject * o, Pedestrian * a)//
{

	a->pedestrian_id			= double_from_attribute(o,"pedestrian_id");
	a->group_id					= double_from_attribute(o,"group_id");
	a->radius                   = double_from_attribute(o, "radius");
  
	a->position         		= vector_from_attribute(o, "position");
	
    a->in_group_a_strength      = double_from_attribute(o, "in_group_a_strength");
    a->in_group_a_range			= double_from_attribute(o, "in_group_a_range");
    a->in_group_r_strength		= double_from_attribute(o, "in_group_r_strength");
    a->in_group_r_range			= double_from_attribute(o, "in_group_r_range");

    a->out_group_a_strength		= double_from_attribute(o,"out_group_a_strength");
    a->out_group_a_range		= double_from_attribute(o,"out_group_a_range");
	a->out_group_r_strength		= double_from_attribute(o,"out_group_r_strength");
	a->out_group_r_range		= double_from_attribute(o,"out_group_r_range");

}

static PyObject * add_group_pedestrian(PyObject * self, PyObject * args)//
{
    PyObject * p_pedestrian;
	int group_id;
	int current_group_num, i=0;
	int population_remaining_groups = 0;
	int population_before_group = 0;
    PyArg_ParseTuple(args, "O:add_group_pedestrian", &p_pedestrian);
	group_id = double_from_attribute(p_pedestrian,"group_id");
	current_group_num = group_population_count[group_id];
		
	update_total_group_member_count(group_id,current_group_num+1);

	//should allocate index properly according to the size of each group, add to the last position of that group in the array of group_pedestrians
	i=0;
	while(i < group_num){
		if(i!=group_id) { //compute population of before and all after to add at correct position
			population_remaining_groups+= group_population_count[i];
			if (i< group_id){
				population_before_group+=group_population_count[i];
			}
		}
		else{
			population_remaining_groups +=0;
		}
		i++;
	}	
	for(i = population_remaining_groups + group_population_count[group_id] -1 ; i >= (group_population_count[group_id]+population_before_group); i--) {
			group_pedestrians[i] = group_pedestrians[i-1];
			
	}
	
	i = group_population_count[group_id] + population_before_group -1;
	pedestrian_from_pyobject(p_pedestrian, &group_pedestrians[i]);

    Py_RETURN_NONE;
}

static void rk_appropximate_level(int level_k, int population_count){//

	int i;
	if(level_k==1){ //compute at level 1
		for(i = 0; i < population_count; i++) {
			//reset acceleration at each  level 1 before computing it
			vector_imul(&group_pedestrians[i].acceleration_rk[0], 0.0);
			group_pedestrians[i].position_temp = group_pedestrians[i].position;
		}

		for(i = 0; i < population_count; i++) {
			// compute interaction attraction force for pedestrian i by 0 index
			calculate_pedestrian_repulsion_attraction(&group_pedestrians[i],i,0,population_count);
		}

		for(i = 0; i < population_count; i++) {
			group_pedestrians[i].position_rk[0] = vector_mul(group_pedestrians[i].acceleration_rk[0], timestep);

		}
	}
	else if(level_k==2){ //compute at level 2
		for(i = 0; i < population_count; i++) {
			//reset acceleration at each  level k before computing it
			vector_imul(&group_pedestrians[i].acceleration_rk[1], 0.0);
			group_pedestrians[i].position_temp = vector_add(group_pedestrians[i].position, vector_mul(group_pedestrians[i].position_rk[0], 0.5));
		}

		for(i = 0; i < population_count; i++) {
			// compute interaction force for pedestrian i at level 2 by 1 index
			calculate_pedestrian_repulsion_attraction(&group_pedestrians[i],i,1,population_count);
		}
		
		for(i = 0; i < population_count; i++) {
			group_pedestrians[i].position_rk[1]= vector_mul(group_pedestrians[i].acceleration_rk[1], timestep);
		}
	}
	else if(level_k==3){ //compute at level 3
		for(i = 0; i < population_count; i++) {
			//reset acceleration at each  level k before computing it
			vector_imul(&group_pedestrians[i].acceleration_rk[2], 0.0);
			group_pedestrians[i].position_temp = vector_add(group_pedestrians[i].position, vector_mul(group_pedestrians[i].position_rk[1], 0.5));
		}

		for(i = 0; i < population_count; i++) {
			// compute interaction force for pedestrian i at level 3 by 2 index
			calculate_pedestrian_repulsion_attraction(&group_pedestrians[i],i,2,population_count);
		}
		for(i = 0; i < population_count; i++) {
			group_pedestrians[i].position_rk[2]  = vector_mul(group_pedestrians[i].acceleration_rk[2], timestep);
		}
	}
	else if(level_k==4){ //compute at level 4
		for(i = 0; i < population_count; i++) {
			//reset acceleration at each  level k before computing it
			vector_imul(&group_pedestrians[i].acceleration_rk[3], 0.0);
			group_pedestrians[i].position_temp = vector_add(group_pedestrians[i].position, group_pedestrians[i].position_rk[2]);
		}

		for(i = 0; i < population_count; i++) {
			// compute interaction force for pedestrian i at level 4 by 3 index
			calculate_pedestrian_repulsion_attraction(&group_pedestrians[i],i,3,population_count);
		}
		
		for(i = 0; i < population_count; i++) {
			group_pedestrians[i].position_rk[3] = vector_mul(group_pedestrians[i].acceleration_rk[3], timestep);
		}
	}

	return;	
}
	
static PyObject * update_pedestrians(PyObject * self, PyObject * args)//
{
	int i, population_count=0;	
	
	for(i=0; i < group_num; i++) {
		population_count+= group_population_count[i];
	}
	// update as RungeKutta, not as for each pedestrian
	// loop for all pedestrians regardless group or not, just check if they have the same group_id

	//compute RK level1
	rk_appropximate_level(1,population_count);
	//compute RK level2
	rk_appropximate_level(2,population_count);
	//compute RK level3
	rk_appropximate_level(3,population_count);
	//compute RK level4
	rk_appropximate_level(4,population_count);

	//update position for in-group pedestrians
	for(i = 0; i < population_count; i++) {
	   update_position(&group_pedestrians[i]);
	}
	
	Py_RETURN_NONE;
}

static void update_position(Pedestrian * a)//
{
	Vector delta_p, delta_p_temp;

	//update position
	delta_p = vector_add(a->position_rk[0],vector_mul(a->position_rk[1],2));
	delta_p_temp = vector_add(vector_mul(a->position_rk[2],2),a->position_rk[3]);
	vector_iadd(&delta_p,&delta_p_temp);
	vector_imul(&delta_p,1/6.0);
	a->position = vector_add(a->position,delta_p);

}

static void  calculate_pedestrian_repulsion_attraction(Pedestrian *a,int index, int level_rk, int population_count)//
{
	int j;
	Vector interaction;
	double repulsion_strength, attraction_strength;
	int group_id; 
	//compute attraction force for group pedestrian
	for(j = 0; j < population_count; j++) {
		if(index == j) continue;
		
		group_id = group_pedestrians[j].group_id;
		repulsion_strength = 0;
		attraction_strength = 0;
		interaction.x = 0.0;
		interaction.y = 0.0; 
		
		if(a->group_id == group_id) {		
			//we compute the repulsion force between this two pedestrians in the same group
			repulsion_strength = calculate_magnitude_repulsion_vector(a,group_pedestrians[j], 1);
		    //we compute the attraction force between this two pedestrians
			attraction_strength = calculate_magnitude_attraction_vector(a,group_pedestrians[j], 1);

			
		} else {
			//we compute the repulsion force between this two pedestrians in different groups
			repulsion_strength = calculate_magnitude_repulsion_vector(a,group_pedestrians[j], 2);
		    //we compute the attraction force between this two pedestrians in different groups
			attraction_strength = calculate_magnitude_attraction_vector(a,group_pedestrians[j], 2);
			
		}
		repulsion_strength -=attraction_strength;
		interaction = vector_sub(a->position_temp, group_pedestrians[j].position_temp);
		vector_unitise(&interaction);
		vector_imul(&interaction,repulsion_strength);
		vector_iadd(&a->acceleration_rk[level_rk], &interaction);
	}
}

//this method is to calculate the attraction force created by Pedestrian b on Pedestrian * a
static double calculate_magnitude_repulsion_vector(Pedestrian *a, Pedestrian b, int group_type)//
{
	double radius_sum = a->radius + b.radius;
	Vector from_b     = vector_sub(a->position_temp, b.position_temp);
	double distance   = fabs(vector_length(from_b) - radius_sum);

	double repulsion_strength = 0;
	if (group_type==1){
		repulsion_strength = a->in_group_r_strength * exp((-distance)/a->in_group_r_range);
	} else {
		repulsion_strength = a->out_group_r_strength * exp((-distance)/a->out_group_r_range);
	}
	return repulsion_strength;
}

//this method is to calculate the attraction force created by Pedestrian b on Pedestrian * a
static double calculate_magnitude_attraction_vector(Pedestrian *a, Pedestrian b, int group_type)//
{
	double radius_sum = a->radius + b.radius;
	Vector from_b     = vector_sub(a->position_temp, b.position_temp);
	double distance   = fabs(vector_length(from_b) - radius_sum);

	double attraction_strength = 0.0;
	if (group_type==1){ 
		attraction_strength = a->in_group_a_strength * exp((-distance)/a->in_group_a_range);
	} else {
		attraction_strength = a->out_group_a_strength * exp((-distance)/a->out_group_a_range);
	}
	return attraction_strength;
}

//this method is to retrieve information of group member a
static PyObject * group_pedestrian_a_property(PyObject * self, PyObject * args)//
{
    int i;
	char * property;
    PyArg_ParseTuple(args, "is:group_pedestrian_a_property", &i, &property);

	if(strcmp(property, "position") == 0) {
		return Py_BuildValue("dd",
				group_pedestrians[i].position.x, group_pedestrians[i].position.y);
	}else if(strcmp(property, "radius") == 0) {
		return PyFloat_FromDouble(group_pedestrians[i].radius);
	}else if (strcmp(property, "groupid") == 0){
		return PyFloat_FromDouble(group_pedestrians[i].group_id);
	} 
	
	PyErr_SetString(PyExc_AttributeError, property);
	return NULL;
}

static PyObject * set_parameters(PyObject * self, PyObject * args)//
{
	PyObject * o;
	int i;
	PyArg_ParseTuple(args, "O:set_parameters", &o);

	timestep    = double_from_attribute(o, "timestep");
	
	//set group_num
	group_num	= double_from_attribute(o, "group");
	
	//set group number for each group
	group_population_count = PyMem_Malloc(group_num * sizeof(int));
	
	for(i=0; i < group_num; i++)
		group_population_count[i] = 0;
	
	group_pedestrians=NULL;
	group_pedestrians = PyMem_Realloc(group_pedestrians, 0 * sizeof(Pedestrian));

	Py_RETURN_NONE;
}

static PyObject * reset_model(PyObject* self)//
{
	int i;
	for(i=0; i < group_num; i++)
		group_population_count[i] = 0;
	
	//group_pedestrians=NULL;
	group_pedestrians = PyMem_Realloc(group_pedestrians, 0 * sizeof(Pedestrian));

	///////////////////// remember to FREE all pointers
	//// free(array);
	Py_RETURN_NONE;
}

static PyMethodDef ForceModelMethods[] = {
    {"add_group_pedestrian", add_group_pedestrian, METH_VARARGS, //
        "Add an group member to the list"},
	{"set_parameters",set_parameters,METH_VARARGS,//
		"Set simulation parameters"},
	{"group_pedestrian_a_property", group_pedestrian_a_property, METH_VARARGS, ////
        "Get an property for group members"},	
	{"get_population_size",(PyCFunction)get_population_size,METH_NOARGS,////
		"Get total population number"},
	{"update_pedestrians",update_pedestrians,METH_VARARGS,//
		"Calculate the acceleration of an pedestrian"},
	{"reset_model",(PyCFunction)reset_model,METH_NOARGS,
		"Reset model for parameters and pedestrians"},
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
    return m;
}
