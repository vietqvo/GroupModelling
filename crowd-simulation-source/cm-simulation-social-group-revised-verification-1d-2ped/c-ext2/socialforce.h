#include <Python.h>
#include <math.h>
#include "vector.h"


typedef struct {
    double radius;
    double time; //travelling duration from initial pos to current pos

    double pedestrian_id; //=pedestrian Id for tracking purpose

    double force_unit; //=A
    double interaction_range; //=B

    double att_unit; //group attraction
    double att_range;//group attraction range


    double position;
    double velocity;
    double acceleration;

	double acceleration_rk[5]; //rk for each order
	double position_rk[4];//rk for each order

	double position_temp; 
	double previous_position;

} Pedestrian;

/**** initial methods****/
static PyObject * add_group_pedestrian(PyObject * self, PyObject * args);
static PyObject * set_parameters(PyObject * self, PyObject * args);
static PyObject * update_pedestrians(PyObject * self, PyObject * args);
static void update_total_group_member_count(Py_ssize_t count);

static void pedestrian_from_pyobject(PyObject * o, Pedestrian * a);
static double double_from_attribute(PyObject * o, char * name);

/**** update model methods ****/
static void rk_appropximate_level(int k);
static void calculate_pedestrian_repulsion(Pedestrian * a,int index, int level_rk);
static void calculate_group_force(Pedestrian *a,int index,int level_rk);
static void identify_group_centre_of_mass();

static double calculate_i_repulsion_vector(Pedestrian *a, Pedestrian b,int level_rk);
static double calculate_i_attraction_vector(Pedestrian *a, Pedestrian b,int level_rk);

static void update_position(Pedestrian * a);

/*** get methods ****/
static PyObject* group_pedestrian_a_property(PyObject * self, PyObject * args);
static PyObject* get_population_size(PyObject* self);
static PyObject* get_group_centre_of_mass(PyObject * self);
static PyObject* get_group_cohesion_degree(PyObject * self);

/*** reset model ***/
static PyObject * reset_model(PyObject* self);
