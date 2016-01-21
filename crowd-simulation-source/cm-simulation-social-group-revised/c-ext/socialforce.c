#include "socialforce.h"

static Pedestrian * group_pedestrians;
static Wall * walls;

static Py_ssize_t group_population_count;

static Py_ssize_t escaped_count;

static Py_ssize_t w_count;

static double U, timestep;

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
    a->radius                   = double_from_attribute(o, "radius");
    a->time                     = double_from_attribute(o, "time");
    a->initial_desired_velocity = double_from_attribute(o, "initial_desired_velocity");
    a->max_velocity             = double_from_attribute(o, "max_velocity");
    a->relax_time               = double_from_attribute(o, "relax_time");

    a->force_unit               = double_from_attribute(o, "force_unit");
    a->interaction_range		= double_from_attribute(o, "interaction_range");

    a->att_unit					= double_from_attribute(o,"attraction_strength");
    a->att_range				= double_from_attribute(o,"attraction_range");

    a->p_type					= double_from_attribute(o, "p_type");
    a->pedestrian_id			= double_from_attribute(o,"pedestrian_id");

    a->position         		= vector_from_attribute(o, "position");
    a->initial_position 		= vector_from_attribute(o, "initial_position");
    a->target           		= vector_from_attribute(o, "target");
    a->velocity         		= vector_from_attribute(o, "velocity");
    a->acceleration     		= vector_from_attribute(o, "acceleration");

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


static PyObject * update_pedestrians(PyObject * self, PyObject * args)
{
	int i;
	
	identify_group_centre_of_mass();
	
	for(i = 0; i < group_population_count; i++) {
		// compute desired force for each pedestrian
		calculate_desired_acceleration(&group_pedestrians[i]);

		// compute interaction force for pedestrian i
		calculate_pedestrian_repulsion(&group_pedestrians[i],i,1);// index i and group pedestrian

		//compute repulsive force from obstacles
		calculate_wall_repulsion(&group_pedestrians[i]);
		
		if (group_population_count >=2) {
			calculate_group_force(&group_pedestrians[i],i);
		}
	}
	
	//update position for in-group pedestrians
	for(i = 0; i < group_population_count; i++) {
	   update_position(&group_pedestrians[i]);
	}

	check_escapes(); //check escape for group members
	
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

}

static void calculate_desired_acceleration(Pedestrian * a){
		double average_velocity = 0.0, desired_velocity = 0.0;
	    Vector desired_direction = {0.0, 0.0};

	    if(a->time) {
	        double proj = vector_projection_length(
	                a->initial_position, a->target, a->position);
	        average_velocity = proj / a->time;

	        a->impatience_level = 1.0 - average_velocity / a->initial_desired_velocity;

	        if (a->impatience_level < 0){
	        	a->impatience_level =0;
	        }

	        desired_velocity = (1.0- a->impatience_level) * a->initial_desired_velocity +
							   (a->impatience_level * a->max_velocity);

	    } else {
			desired_velocity = a->initial_desired_velocity;
		}
	    desired_direction = vector_sub(a->target, a->position);
	    vector_unitise(&desired_direction);

		a->acceleration = vector_mul(desired_direction, desired_velocity);
	    vector_isub(&a->acceleration, &a->velocity);
	    vector_imul(&a->acceleration, 1.0/a->relax_time);

}

static void calculate_pedestrian_repulsion(Pedestrian * a,int index, int group_type)
{
	int j;
	Vector repulsion;

	//compute repulsion force for group pedestrian
	for(j = 0; j < group_population_count; j++) {
	        if(index == j && group_type ==1) continue;
	        
			//we compute the force between this two pedestrians
	        repulsion = calculate_i_repulsion_vector(a,group_pedestrians[j]);
	        vector_iadd(&a->acceleration, &repulsion);
	}
}

//this method is to calculate the repulsion force created by Pedestrian b on Pedestrian * a
static Vector calculate_i_repulsion_vector(Pedestrian *a, Pedestrian b)
{
	double radius_sum = a->radius + b.radius;
	Vector from_b     = vector_sub(a->position, b.position);
	//Vector from_b     = vector_sub(b.position, a->position);
	double distance   = vector_length(from_b);

	vector_unitise(&from_b);
	vector_imul(&from_b, a->force_unit * exp((radius_sum-distance)/a->interaction_range));

	return from_b;
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

static void  calculate_group_force(Pedestrian *a,int index)
{
	Vector attraction;
	int j;
	//compute attraction force for group pedestrian
	for(j = 0; j < group_population_count; j++) {
		   if(index == j) continue;
			//we compute the attraction force between this two pedestrians
		   attraction = calculate_i_attraction_vector(a,group_pedestrians[j]);
	       vector_iadd(&a->acceleration, &attraction);
	}
}

//this method is to calculate the attraction force created by Pedestrian b on Pedestrian * a
static Vector calculate_i_attraction_vector(Pedestrian *a, Pedestrian b)
{
	double radius_sum = a->radius + b.radius;
	Vector from_b     = vector_sub(b.position, a->position);
	double distance   = vector_length(from_b);

	vector_unitise(&from_b);
	vector_imul(&from_b, a->att_unit * exp((radius_sum-distance)/a->att_range));

	return from_b;
}

static void check_escapes()
{
	int i, j;
	
	for(i = 0, j = 0; i < group_population_count; i++) {
		if(!is_escaped(&group_pedestrians[i])) {
			group_pedestrians[j++] = group_pedestrians[i];
		}
	}
	if(i!=j)
	{
		update_total_group_member_count(group_population_count - (i-j));
		escaped_count += i-j;
	}
}

static int is_escaped(Pedestrian * a)
{

	double l = vector_length(vector_sub(a->target, a->position));
	if (l <= a->radius*2) return 1;
    return 0;
}

static void calculate_wall_repulsion(Pedestrian * a){
	 int i;
	 Vector * repulsion_points  = PyMem_Malloc(w_count * sizeof(Vector));
	 int rep_p_c = 0;
	 Vector repulsion;

	 rep_p_c = find_repulsion_points(a, repulsion_points);

	 for(i = 0; i < rep_p_c; i++) {
	     repulsion = calculate_wall_repulsion_point(a, repulsion_points[i]);
	     vector_iadd(&a->acceleration, &repulsion);
	 }

	 PyMem_Free(repulsion_points);
}

static Vector calculate_wall_repulsion_point(Pedestrian * a, Vector repulsion_point)
{
	Vector repulsion_vector;
	double repulsion_length;
	double repulsion_force;

	repulsion_vector = vector_sub(a->position, repulsion_point);
	repulsion_length = vector_length(repulsion_vector);
	vector_unitise_c(&repulsion_vector, repulsion_length);

	repulsion_force = (1/a->radius) * U * exp(-repulsion_length/a->radius);
	vector_imul(&repulsion_vector, repulsion_force);

	return repulsion_vector;
}

static int find_repulsion_points(Pedestrian * a, Vector repulsion_points[]){
	int i,j;
	double projection_length;
	Vector * used_endpoints    = PyMem_Malloc(2*w_count * sizeof(Vector));
	Vector * possible_endpoints = PyMem_Malloc(w_count * sizeof(Vector));
	int rep_p_c = 0, use_e_c = 0, pos_e_c = 0;

	for(i = 0; i < w_count; i++) {
	    Wall w = walls[i];
	    projection_length = vector_projection_length(w.start, w.end, a->position);
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
			if(!free_e ||
				vector_length(vector_sub(a->position,
						possible_endpoints[i])) < a->radius) {
				repulsion_points[rep_p_c++] = possible_endpoints[i];
				used_endpoints[use_e_c++] = possible_endpoints[i];
			}
	   }
	}

	PyMem_Free(used_endpoints);
	PyMem_Free(possible_endpoints);

	return rep_p_c;
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
	}else if(strcmp(property,"relax_time")==0) {
		return PyFloat_FromDouble(group_pedestrians[i].relax_time);

	} else if(strcmp(property, "velocity") == 0) {
		return PyFloat_FromDouble(vector_length(group_pedestrians[i].velocity));

	} else if(strcmp(property,"initial_velocity")==0) {
		return PyFloat_FromDouble(group_pedestrians[i].initial_desired_velocity);

	} else if(strcmp(property,"max_velocity")==0) {
		return PyFloat_FromDouble(group_pedestrians[i].max_velocity);

	}else if (strcmp(property,"impatience_level")==0) {
		return PyFloat_FromDouble(group_pedestrians[i].impatience_level);

	} else if (strcmp(property, "p_type") == 0){
		return PyFloat_FromDouble(group_pedestrians[i].p_type);

	}else if(strcmp(property, "target") == 0) {
		return Py_BuildValue("dd",
				group_pedestrians[i].target.x, group_pedestrians[i].target.y);
	} else if(strcmp(property, "id") ==0){
		return PyFloat_FromDouble(group_pedestrians[i].pedestrian_id);
	}

	PyErr_SetString(PyExc_AttributeError, property);
	return NULL;
}

static PyObject * check_escaped(PyObject * self, PyObject * args)
{
	  double ped_id;
	  int index;
	  PyArg_ParseTuple(args, "d:check_escaped", &ped_id);

	  for(index = 0; index < group_population_count; index++) {
		  if(group_pedestrians[index].pedestrian_id == ped_id){
			  return Py_BuildValue("i",0);
		  }
	  }
	  
	  return Py_BuildValue("i",1);
}

static PyObject * get_group_centre_of_mass(PyObject * self)
{
	return Py_BuildValue("dd",
				group_centre_of_mass.x, group_centre_of_mass.y);
}

static PyObject * get_group_average_direction(PyObject * self)
{	
	Vector group_average_direction;
	int j;
	double group_average_direction_value;
	
	group_average_direction.x=0;
	group_average_direction.y=0;
	
	//compute average direction for group pedestrian
	for(j = 0; j < group_population_count; j++)
	{
		group_average_direction.x += group_pedestrians[j].velocity.x;
		group_average_direction.y += group_pedestrians[j].velocity.y;
	}
		
	//get magnitude of group_average_direction vector
	group_average_direction_value = vector_length(group_average_direction);
	
	return PyFloat_FromDouble(group_average_direction_value/group_population_count);	
}

static PyObject * get_group_average_speed(PyObject * self)
{
	double group_average_speed=0;
	int j;
	//compute average speed for group pedestrian
	for(j = 0; j < group_population_count; j++)
		group_average_speed += vector_length(group_pedestrians[j].velocity);
	
	return PyFloat_FromDouble(group_average_speed/group_population_count);	
	
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
	PyObject * o, * p_walls;
	PyArg_ParseTuple(args, "O:set_parameters", &o);

	U           = double_from_attribute(o, "U");
	timestep    = double_from_attribute(o, "timestep");
	
	//create wall obstacle
	p_walls     = PyDict_GetItemString(o, "walls");
	w_count = PyList_Size(p_walls);
	walls    = PyMem_Realloc(walls, w_count * sizeof(Wall));
	init_walls(p_walls, walls, w_count);

	update_total_group_member_count(0);
	
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
	group_population_count     = -1; //reset total group member number
	escaped_count = 0; //reset escaped pedestrian number
			
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
	{"get_escaped_num",(PyCFunction)get_escaped_num,METH_NOARGS,
		"Get total escaped number"},
	{"reset_model",(PyCFunction)reset_model,METH_NOARGS,
		"Reset model for parameters and pedestrians"},
	{"check_escaped", check_escaped, METH_VARARGS,
		"Check a pedestrian escaped by ped_id"},
	{"get_group_centre_of_mass", (PyCFunction)get_group_centre_of_mass, METH_NOARGS,
		"Get group centre of mass over the time"},
	{"get_group_average_direction", (PyCFunction)get_group_average_direction, METH_NOARGS,
		"Get group average direction over the time"},
	{"get_group_average_speed", (PyCFunction)get_group_average_speed, METH_NOARGS,
		"Get group average speed over the time"},
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

    group_population_count     = -1; //reset total group member number
	escaped_count = 0; //reset escaped pedestrian number

	group_centre_of_mass.x =0;
	group_centre_of_mass.y=0;
	
    group_pedestrians=NULL;
	
    timestep    = 0; //reset timestep
	
	update_total_group_member_count(0);
	
    return m;
}
