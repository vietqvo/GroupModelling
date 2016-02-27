#include <Python.h>
#include <math.h>
#include "vector.h"

#define PI 3.14159265

typedef struct {
    double p_type; //=pedestrian type
    double pedestrian_id; //=pedestrian Id for tracking purpose
	int group_id;
	
    double radius;
    double time; //travelling duration from initial position to current position
    double initial_desired_velocity;
    double max_velocity;
    double relax_time;

    double force_unit; //=A
    double interaction_range; //=B

    double att_force_unit;
    double att_interaction_range;

    double att_unit; //group attraction
    double att_range;//group attraction range

    double impatience_level;//illustrate panic at time t

    Vector position;
    Vector initial_position;
    Vector target;
    Vector velocity;
    Vector acceleration;
	
	Vector acceleration_rk[4]; //rk for each order
	Vector position_rk[4];//rk for each order

	Vector velocity_temp; //this is temporary velocity used to calculate acceleration at each RK order
	Vector position_temp; //this is temporary position used to calculate acceleration at each RK order
	double time_temp;//this is temporary time used to calculate desired velocity in desired acceleration at each RK order
	
} Pedestrian;

typedef struct {
    Vector start;
    Vector end;
    double length;
} Wall;

/**** initial methods****/
static PyObject * add_group_pedestrian(PyObject * self, PyObject * args);//
static PyObject * set_parameters(PyObject * self, PyObject * args);//
static PyObject * update_pedestrians(PyObject * self, PyObject * args);//
static void update_total_group_member_count(Py_ssize_t groupIndex, int count);//

static void pedestrian_from_pyobject(PyObject * o, Pedestrian * a);//
static double double_from_attribute(PyObject * o, char * name);//
static Vector vector_from_attribute(PyObject * o, char * name);//

static Wall wall_from_pyobject(PyObject *o);//
static Vector vector_from_pyobject(PyObject * o);//
static void init_walls(PyObject * p_walls, Wall * walls_p, Py_ssize_t w_count);//


/**** update model methods ****/
static void calculate_desired_acceleration(Pedestrian * a,int level_rk);//
static void calculate_pedestrian_repulsion(Pedestrian * a,int index, int level_rk,int population_count);//
static void calculate_wall_repulsion(Pedestrian * a, int level_rk);//
static void calculate_group_force(Pedestrian *a,int index, int level_rk, int population_count);//
static void identify_group_centre_of_mass(int population_size);//


static int find_repulsion_points(Pedestrian * a, Vector repulsion_points[]);//
static Vector calculate_repulsion_vector(Pedestrian a, Pedestrian b);
static Vector calculate_i_repulsion_vector(Pedestrian *a, Pedestrian b);//
static double calculate_magnitude_attraction_vector(Pedestrian *a, Pedestrian b);//
static double calculate_magnitude_repulsion_vector(Pedestrian *a, Pedestrian b);


static Vector calculate_wall_repulsion_point(Pedestrian * a, Vector repulsion_point);//

static void update_position(Pedestrian * a);//
static void rk_appropximate_level(int level_k, int population_count);//
static void check_escapes(int population_count);//
static int is_escaped(Pedestrian * a);//

/*** get methods ****/
static PyObject* group_pedestrian_a_property(PyObject * self, PyObject * args);//
static PyObject* get_population_size(PyObject* self);//
static PyObject* get_group_escaped_num(PyObject* self);//
static PyObject* get_group_centre_of_mass(PyObject * self, PyObject * args);//
static PyObject* get_group_cohesion_degree(PyObject * self);//

/*** reset model ***/
static PyObject * reset_model(PyObject* self);//
