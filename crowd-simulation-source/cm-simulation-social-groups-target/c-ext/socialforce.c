#include "socialforce.h"

static int group_num;
static int * group_population_count; //array to contain group size of each group --default = -1
static Pedestrian * group_pedestrians; //array to contain whole pedestrians of different groups 

static Vector * group_centre_of_mass; //array to contain group_center_of_mass of each group
static double * escaped_counts; //array to contain escape_number of each group

static Wall * walls;
static Py_ssize_t w_count;
static double U, timestep; //parameter to compute obstacle force


static void update_total_group_member_count(Py_ssize_t groupIndex, int count)//
{
//group index should run from 0
//default should set group_num = 0, and each group array size = 0

	int population_count=0;
	int i = 0, group_size;
	if (groupIndex < group_num && group_population_count !=NULL) {
		group_size = group_population_count[groupIndex];
		if(count == group_size) return;
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
	int i;
    a->radius                   = double_from_attribute(o, "radius");
    a->time                     = double_from_attribute(o, "time");
    a->initial_desired_velocity = double_from_attribute(o, "initial_desired_velocity"); //use this number as magnitude of desired force
    a->max_velocity             = double_from_attribute(o, "max_velocity");
    a->relax_time               = double_from_attribute(o, "relax_time"); ////use this number as range of desired force

    a->force_unit               = double_from_attribute(o, "force_unit");
    a->interaction_range		= double_from_attribute(o, "interaction_range");

    a->att_force_unit			= double_from_attribute(o, "att_force_unit");
    a->att_interaction_range	= double_from_attribute(o, "att_interaction_range");

    a->att_unit					= double_from_attribute(o,"attraction_strength");
    a->att_range				= double_from_attribute(o,"attraction_range");

    a->p_type					= double_from_attribute(o, "p_type");
    a->pedestrian_id			= double_from_attribute(o,"pedestrian_id");
	a->group_id					= double_from_attribute(o,"group_id");
	
    a->position         		= vector_from_attribute(o, "position");
    a->initial_position 		= vector_from_attribute(o, "initial_position");
    a->target           		= vector_from_attribute(o, "target");
    a->velocity         		= vector_from_attribute(o, "velocity");
    a->acceleration     		= vector_from_attribute(o, "acceleration");
	
	//initial level of runge kutta method, 0 element is for initial
	for(i=0; i <4; i++){
		a->acceleration_rk [i] = vector_mul(a->acceleration,0.0);
		a->position_rk[i] = vector_mul(a->position,0.0);
	}
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

	//should allocate properly according to the size of each group, add to the last position of that group in the array of group_pedestrians
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

static void identify_group_centre_of_mass(int population_size)//
{
	int i;
	int group_id;
	for(i=0; i < group_num;i++)
	{
		group_centre_of_mass[i].x = 0;
		group_centre_of_mass[i].y=0;
	}
	
	//if belong to which group_id, we add on for corresponding group_center_of_mass
	for(i=0; i < population_size;i++){
		group_id = group_pedestrians[i].group_id;
		vector_iadd(&group_centre_of_mass[group_id],&group_pedestrians[i].position);
	}
	
	for(i=0; i < group_num;i++)
	{
		vector_unitise_c(&group_centre_of_mass[i],group_population_count[i]);	
	}	
}

static void rk_appropximate_level(int level_k, int population_count){//

	int i;
	if(level_k==1){ //compute at level 1
		for(i = 0; i < population_count; i++) {
			//reset acceleration at each  level 1 before computing it
			vector_imul(&group_pedestrians[i].acceleration_rk[0], 0.0);
			group_pedestrians[i].position_temp = group_pedestrians[i].position;
			group_pedestrians[i].time_temp	= group_pedestrians[i].time;
		}

		for(i = 0; i < population_count; i++) {

			// compute desired force for pedestrian i at level 1 by 0 index
			calculate_desired_acceleration(&group_pedestrians[i],0);  

			// compute interaction force for pedestrian i at level 1 by 0 index
			calculate_pedestrian_repulsion(&group_pedestrians[i],i,0,population_count);

			// compute attraction force for pedestrian i at level 1 by 0 index
			calculate_group_force(&group_pedestrians[i],i,0,population_count);
			
			//compute repulsive force from obstacles at level 1 by 0 index
			calculate_wall_repulsion(&group_pedestrians[i],0);
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
			group_pedestrians[i].time_temp	= group_pedestrians[i].time  + (timestep/2);
		}

		for(i = 0; i < population_count; i++) {

			// compute desired force for pedestrian i at level 2 by 1 index
			calculate_desired_acceleration(&group_pedestrians[i],1);  

			// compute interaction force for pedestrian i at level 2 by 1 index
			calculate_pedestrian_repulsion(&group_pedestrians[i],i,1,population_count);

			// compute attraction force for pedestrian i at level 2 by 1 index
			calculate_group_force(&group_pedestrians[i],i,1,population_count);
			
			//compute repulsive force from obstacles at level 2 by 1 index
			calculate_wall_repulsion(&group_pedestrians[i],1);
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
			group_pedestrians[i].time_temp	= group_pedestrians[i].time  + (timestep/2);
		}

		for(i = 0; i < population_count; i++) {
			// compute desired force for pedestrian i at level 3 by 2 index
			calculate_desired_acceleration(&group_pedestrians[i],2);
			
			// compute interaction force for pedestrian i at level 3 by 2 index
			calculate_pedestrian_repulsion(&group_pedestrians[i],i,2,population_count);
			
			// compute attraction force for pedestrian i at level 3 by 2 index
			calculate_group_force(&group_pedestrians[i],i,2,population_count);
			
			//compute repulsive force from obstacles at level 3 by 2 index
			calculate_wall_repulsion(&group_pedestrians[i],2);
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
			group_pedestrians[i].time_temp	= group_pedestrians[i].time  + timestep;
		}

		for(i = 0; i < population_count; i++) {
			// compute desired force for pedestrian i at level 4 by 3 index
			calculate_desired_acceleration(&group_pedestrians[i],3);
			
			// compute interaction force for pedestrian i at level 4 by 3 index
			calculate_pedestrian_repulsion(&group_pedestrians[i],i,3,population_count);
			
			// compute attraction force for pedestrian i at level 4 by 3 index
			calculate_group_force(&group_pedestrians[i],i,3,population_count);
			
			//compute repulsive force from obstacles at level 4 by 3 index
			calculate_wall_repulsion(&group_pedestrians[i],3);
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
	
	identify_group_centre_of_mass(population_count);
	
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
	//check escape for group members
	check_escapes(population_count); 
	
	Py_RETURN_NONE;
}
	
static void update_position(Pedestrian * a)//
{
	Vector delta_v, delta_v_temp, delta_p, delta_p_temp;

	//update position
	delta_p = vector_add(a->position_rk[0],vector_mul(a->position_rk[1],2));
	delta_p_temp = vector_add(vector_mul(a->position_rk[2],2),a->position_rk[3]);
	vector_iadd(&delta_p,&delta_p_temp);
	vector_imul(&delta_p,1/6.0);
	a->position = vector_add(a->position,delta_p);

	a->time += timestep;

}

static void calculate_desired_acceleration(Pedestrian * a,int level_rk){//

	Vector from_ped    = vector_sub(a->position_temp,  a->target);
	double distance   = fabs(vector_length(from_ped) - a->radius);

	double desired_force =  a->initial_desired_velocity * exp(distance/a->relax_time);

	vector_unitise(&from_ped);
	vector_imul(&from_ped, desired_force);

	a->acceleration_rk[level_rk] = vector_mul(from_ped, 1.0);
}

static void calculate_pedestrian_repulsion(Pedestrian * a,int index, int level_rk,int population_count)//
{
	int j, group_id;
	Vector repulsion;

	//compute repulsion force for group pedestrian
	for(j = 0; j < population_count; j++) {
		group_id = group_pedestrians[j].group_id;

	    if(index == j || a->group_id == group_id) continue;

		//we compute the force between this two pedestrians out-of-group pedestrians
	    repulsion = calculate_i_repulsion_vector(a,group_pedestrians[j]);
	    vector_iadd(&a->acceleration_rk[level_rk], &repulsion);
	}
}

//this method is to calculate the repulsion force created by Pedestrian b on Pedestrian * a
static Vector calculate_i_repulsion_vector(Pedestrian *a, Pedestrian b)//
{
	double radius_sum = a->radius + b.radius;
	Vector from_b     = vector_sub(a->position_temp, b.position_temp);
	double distance   = vector_length(from_b);

	vector_unitise(&from_b);
	vector_imul(&from_b, a->force_unit * exp((radius_sum-distance)/a->interaction_range));

	return from_b;
}

static void  calculate_group_force(Pedestrian *a,int index, int level_rk, int population_count)//
{
	int j;
	Vector interaction;
	double repulsion_strength;
	double attraction_strength;
	int group_id; 
	//compute attraction force for group pedestrian
	for(j = 0; j < population_count; j++) {
		if(index == j) continue;
		
		group_id = group_pedestrians[j].group_id;
		
		if(a->group_id == group_id) {		
			//we compute the repulsion force between this two pedestrians
			repulsion_strength = calculate_magnitude_repulsion_vector(a,group_pedestrians[j]);

		   //we compute the attraction force between this two pedestrians
			attraction_strength = calculate_magnitude_attraction_vector(a,group_pedestrians[j]);

			repulsion_strength -=attraction_strength;

			interaction = vector_sub(a->position_temp, group_pedestrians[j].position_temp);
			vector_unitise(&interaction);

			vector_imul(&interaction,repulsion_strength);

			vector_iadd(&a->acceleration_rk[level_rk], &interaction);
		}
	}
}

//this method is to calculate the attraction force created by Pedestrian b on Pedestrian * a
static double calculate_magnitude_repulsion_vector(Pedestrian *a, Pedestrian b)//
{
	double radius_sum = a->radius + b.radius;
	Vector from_b     = vector_sub(a->position_temp, b.position_temp);
	double distance   = fabs(vector_length(from_b) - radius_sum);

	double force_strength =  a->att_force_unit * exp((-distance)/a->att_interaction_range);

	return force_strength;
}


//this method is to calculate the attraction force created by Pedestrian b on Pedestrian * a
static double calculate_magnitude_attraction_vector(Pedestrian *a, Pedestrian b)//
{
	double radius_sum = a->radius + b.radius;
	Vector from_b     = vector_sub(a->position_temp, b.position_temp);
	double distance   = fabs(vector_length(from_b) - radius_sum);

	double force_strength =  a->att_unit * exp((-distance)/a->att_range);

	return force_strength;
}

static void calculate_wall_repulsion(Pedestrian * a, int level_rk){//
	 int i;
	 Vector * repulsion_points  = PyMem_Malloc(w_count * sizeof(Vector));
	 int rep_p_c = 0;
	 Vector repulsion;

	 rep_p_c = find_repulsion_points(a, repulsion_points);

	 for(i = 0; i < rep_p_c; i++) {
	     repulsion = calculate_wall_repulsion_point(a, repulsion_points[i]);
	     vector_iadd(&a->acceleration_rk[level_rk], &repulsion);
	 }

	 PyMem_Free(repulsion_points);
}

static int find_repulsion_points(Pedestrian * a, Vector repulsion_points[]){//
	int i,j;
	double projection_length;
	Vector * used_endpoints    = PyMem_Malloc(2*w_count * sizeof(Vector));
	Vector * possible_endpoints = PyMem_Malloc(w_count * sizeof(Vector));
	int rep_p_c = 0, use_e_c = 0, pos_e_c = 0;

	for(i = 0; i < w_count; i++) {
	    Wall w = walls[i];
	    projection_length = vector_projection_length(w.start, w.end, a->position_temp);
	    if(projection_length < 0)  {
	         possible_endpoints[pos_e_c++] = w.start;
	    } else if(projection_length > w.length) {
	        possible_endpoints[pos_e_c++] = w.end;
	    } else {
	            // We have the length, L, of how far along AB the projection point is.
	            // To turn this into a point, we multiply AB with L/|AB| and add
	            // this vector to the starting point A.
				// P = A + AB*L/|AB|
	       repulsion_points[rep_p_c++] = vector_add(w.start,
	                vector_mul(vector_sub(w.end, w.start),
	                projection_length/w.length));
	       used_endpoints[use_e_c++] = w.start;
	       used_endpoints[use_e_c++] = w.end;
	     }
	}

	for(i = 0; i < pos_e_c; i++) {
	   int use_e = 1;
	   for(j = 0; j < use_e_c; j++) {
		   if(vector_equals(possible_endpoints[i], used_endpoints[j])) {
	             use_e = 0;
	       }
	   }
	   if(use_e) {
		// Keep track of whether the endpoint is free-floating, i.e. if
		// it is shared with another wall as near bottle neck
		   int free_e = 1;
			for(j = 0; j < pos_e_c; j++) {
				if(i != j && vector_equals(possible_endpoints[i],
								possible_endpoints[j])) {
					free_e = 0;
				}
			}
				// Endpoints that are free-floating (i.e. sides of doorways) are
				// only considered for repulsion if they are closer to the pedestrian
				// than the pedestrian's radius. This allows pedestrians to pass more
				// freely through doorways.
				// *** a minimum gap between two walls ****
			if(!free_e || vector_length(vector_sub(a->position_temp,possible_endpoints[i])) < a->radius)
			{
				repulsion_points[rep_p_c++] = possible_endpoints[i];
				used_endpoints[use_e_c++] = possible_endpoints[i];
			}
	   }
	}

	PyMem_Free(used_endpoints);
	PyMem_Free(possible_endpoints);

	return rep_p_c;
}

static Vector calculate_wall_repulsion_point(Pedestrian * a, Vector repulsion_point)//
{
	Vector repulsion_vector;
	double repulsion_length;
	double repulsion_force;

	repulsion_vector = vector_sub(a->position_temp, repulsion_point);
	repulsion_length = vector_length(repulsion_vector);
	vector_unitise_c(&repulsion_vector, repulsion_length);

	repulsion_force = (1/a->radius) * U * exp(-repulsion_length/a->radius);
	vector_imul(&repulsion_vector, repulsion_force);

	return repulsion_vector;
}

static void check_escapes(int population_count)//
{
	int i, j;
	int * temp_escaped_of_groups;
	int group_id;
	
	temp_escaped_of_groups = PyMem_Malloc(group_num * sizeof(int));
	for(i=0; i <group_num; i++){
		temp_escaped_of_groups[i]= 0;
	}
	
	for(i = 0, j = 0; i < population_count; i++) {
		if(!is_escaped(&group_pedestrians[i])) {
			group_pedestrians[j++] = group_pedestrians[i];
		} else{
			group_id = group_pedestrians[i].group_id;
			temp_escaped_of_groups[group_id] +=1;
		}
	}
	
	for(i=0; i < group_num; i++)
	{
		//UPDATE NUMBER OF EACH GROUP, TOTAL POPULATION, ESCAPE NUM
		if (temp_escaped_of_groups[i] !=0){
			update_total_group_member_count(i, group_population_count[i] - temp_escaped_of_groups[i]);
			escaped_counts[i] += temp_escaped_of_groups[i];
		}
	}
	
	PyMem_Free(temp_escaped_of_groups);
}

static int is_escaped(Pedestrian * a)//
{

	double l = vector_length(vector_sub(a->target, a->position));
	if (l <= a->radius*2) return 1;
    return 0;
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
	} else if(strcmp(property, "velocity") == 0) {
		return PyFloat_FromDouble(vector_length(group_pedestrians[i].velocity));
	} else if (strcmp(property, "groupid") == 0){
		return PyFloat_FromDouble(group_pedestrians[i].group_id);
	} 
	
	PyErr_SetString(PyExc_AttributeError, property);
	return NULL;
}

static PyObject * get_group_centre_of_mass(PyObject * self, PyObject * args)//
{
	Py_ssize_t group_id;
    PyArg_ParseTuple(args, "i:get_group_centre_of_mass", &group_id);
	
	return Py_BuildValue("dd",
				group_centre_of_mass[group_id].x, group_centre_of_mass[group_id].y);
}

static PyObject * get_group_cohesion_degree(PyObject * self)//
{
	double population_count;
	Vector distance;
	double * group_cohesion_degree;
	PyObject* tuple = PyTuple_New(group_num); 
	int group_id;
	int i;
	
	group_cohesion_degree = PyMem_Malloc(group_num * sizeof(double));
	for(i=0; i <group_num; i++){
		group_cohesion_degree[i]= 0;
	}

	for(i=0; i < group_num; i++) {
		population_count+= group_population_count[i];
	}	
	
	//compute group cohesion degree for pedestrians belong to this group
	for(i = 0; i < population_count; i++)
	{
		group_id = group_pedestrians[i].group_id;
		distance = vector_sub(group_pedestrians[i].position,group_centre_of_mass[group_id]);
		group_cohesion_degree[group_id] = group_cohesion_degree[group_id] + vector_length(distance);
	}
	
	for(i=0; i < group_num; i++) {
		//check to return 0 rather than return e-09 value
		if (group_population_count[i] == 0.0 || group_population_count[i]== 1.0) {
			PyTuple_SET_ITEM(tuple, i, Py_BuildValue("d", 0.0)); 
		} else {
			PyTuple_SET_ITEM(tuple, i, Py_BuildValue("d", group_cohesion_degree[i]/ group_population_count[i])); 
		}
			
	}	
	
	PyMem_Free(group_cohesion_degree);
	
	return tuple; 	
}

static PyObject* get_group_escaped_num(PyObject* self)// 
{
	int i;
	PyObject* tuple = PyTuple_New(group_num);
	
	for(i=0; i < group_num; i++) {
		PyTuple_SET_ITEM(tuple, i, Py_BuildValue("d", escaped_counts[i])); 
	}
	return tuple;
}

static PyObject * set_parameters(PyObject * self, PyObject * args)//
{
	PyObject * o, * p_walls;
	int i;
	PyArg_ParseTuple(args, "O:set_parameters", &o);

	U           = double_from_attribute(o, "U");
	timestep    = double_from_attribute(o, "timestep");
	
	//set group_num
	group_num	= double_from_attribute(o, "group");
	
	//set group number for each group
	group_population_count = PyMem_Malloc(group_num * sizeof(int));
	group_centre_of_mass = PyMem_Malloc(group_num * sizeof(Vector));
	escaped_counts  = PyMem_Malloc(group_num * sizeof(double));
	
	for(i=0; i < group_num; i++)
	{
		group_population_count[i] = 0;
		group_centre_of_mass[i].x = 0;
		group_centre_of_mass[i].y = 0;
		escaped_counts[i] = 0;
	}
	
	group_pedestrians=NULL;
	group_pedestrians = PyMem_Realloc(group_pedestrians, 0 * sizeof(Pedestrian));
	
	
	//create wall obstacle
	p_walls     = PyDict_GetItemString(o, "walls");
	w_count = PyList_Size(p_walls);
	walls    = PyMem_Realloc(walls, w_count * sizeof(Wall));
	init_walls(p_walls, walls, w_count);
	
	Py_RETURN_NONE;
}

static Wall wall_from_pyobject(PyObject *o)//
{
    Wall w;
    w.start.x = PyFloat_AsDouble(PyTuple_GetItem(o, 0));
    w.start.y = PyFloat_AsDouble(PyTuple_GetItem(o, 1));
    w.end.x   = PyFloat_AsDouble(PyTuple_GetItem(o, 2));
    w.end.y   = PyFloat_AsDouble(PyTuple_GetItem(o, 3));
    w.length  = vector_length(vector_sub(w.end, w.start));

    return w;
}

static void init_walls(PyObject * p_walls, Wall * walls_p, Py_ssize_t w_count)//
{
    int i;
    for(i = 0; i < w_count; i++) {
        PyObject * p_w   = PyList_GetItem(p_walls, i);
        Wall w = wall_from_pyobject(p_w);
        walls_p[i] = w;
    }
}

static PyObject * reset_model(PyObject* self)//
{
	int i;
	for(i=0; i < group_num; i++)
	{
		group_population_count[i] = 0;
		group_centre_of_mass[i].x = 0;
		group_centre_of_mass[i].y = 0;
		escaped_counts[i] = 0;
	}
	
	group_pedestrians=NULL;
	group_pedestrians = PyMem_Realloc(group_pedestrians, 0 * sizeof(Pedestrian));
	
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
	{"get_group_escaped_num",(PyCFunction)get_group_escaped_num,METH_NOARGS,
		"Get total escaped number of groups"},
	{"reset_model",(PyCFunction)reset_model,METH_NOARGS,
		"Reset model for parameters and pedestrians"},
	{"get_group_centre_of_mass", (PyCFunction)get_group_centre_of_mass, METH_VARARGS,
		"Get group centre of mass of a group"},
	{"get_group_cohesion_degree", (PyCFunction)get_group_cohesion_degree, METH_NOARGS,
		"Get group cohesion degree over the time"},	
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
