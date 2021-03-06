#include <Python.h>
#include <math.h>
#include "vector.h"

#define ESCAPE_THRESHOLD 50
#define PI 3.14159265

typedef struct {
    double radius;
    double time; //traveling duration from initial pos to current pos
    double force_unit; //=A
    double interaction_range; //=B

    double att_unit; //group attraction
    double att_range;//group attraction range

    double p_type; //=pedestrian type
    double pedestrian_id; //=pedestrian Id for tracking purpose

    Vector position;
    Vector initial_position;
    Vector velocity;
    Vector acceleration;

	Vector acceleration_rk[4]; //rk for each order
	Vector position_rk[4];//rk for each order

	Vector position_temp; //this is temporary position used to calculate acceleration at each order

} Pedestrian;

/**** initial methods****/
static PyObject * add_group_pedestrian(PyObject * self, PyObject * args);
static PyObject * set_parameters(PyObject * self, PyObject * args);
static PyObject * update_pedestrians(PyObject * self, PyObject * args);
static void update_total_group_member_count(Py_ssize_t count);

static void pedestrian_from_pyobject(PyObject * o, Pedestrian * a);
static double double_from_attribute(PyObject * o, char * name);
static Vector vector_from_attribute(PyObject * o, char * name);

static Vector vector_from_pyobject(PyObject * o);

/**** update model methods ****/
static void rk_appropximate_level(int k);
static void calculate_pedestrian_repulsion_attraction(Pedestrian * a,int index, int level_rk);
static void identify_group_centre_of_mass();

static double calculate_repulsion_magnitude(Pedestrian *a, Pedestrian b);
static double calculate_attraction_magnitude(Pedestrian *a, Pedestrian b);

static void update_position(Pedestrian * a);

/*** get methods ****/
static PyObject* group_pedestrian_a_property(PyObject * self, PyObject * args);
static PyObject* get_population_size(PyObject* self);
static PyObject* get_group_centre_of_mass(PyObject * self);
static PyObject* get_group_cohesion_degree(PyObject * self);

/*** reset model ***/
static PyObject * reset_model(PyObject* self);





