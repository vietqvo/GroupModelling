#include <Python.h>
#include <math.h>
#include "vector.h"


typedef struct {
    double radius;
    double time; //traveling duration from initial pos to current pos
    double initial_desired_velocity;
    double relax_time;
    double interaction_constant; //=A
    double interaction_distance;//=R
    double p_type; //=pedestrian type
	int flowline[5]; //line to measure the flow of pedestrian standing on the line
    Vector position;
    Vector free_velocity;
    Vector target;
    Vector velocity;
    Vector acceleration;
} Pedestrian;

typedef struct {
    Vector start;
    Vector end;
    double length;
} Wall;


/*** initial methods ***/
static PyObject * add_pedestrian(PyObject * self, PyObject * args);
static PyObject * set_parameters(PyObject * self, PyObject * args);
static void pedestrian_from_pyobject(PyObject * o, Pedestrian * a);

static double double_from_attribute(PyObject * o, char * name);
static Vector vector_from_attribute(PyObject * o, char * name);
static Wall wall_from_pyobject(PyObject *o);
static Vector vector_from_pyobject(PyObject * o);
static void init_walls(PyObject * p_walls, Wall * walls_p, Py_ssize_t w_count);

/*** update by nomad model ***/
static PyObject * update_pedestrians(PyObject * self, PyObject * args);
static void calculate_desired_acceleration(Pedestrian * a);
static void calculate_pedestrian_repulsion(int index);
static void update_total_count(Py_ssize_t count);
static int is_front_of(Pedestrian a, Pedestrian b);
static Vector calculate_repulsion_vector(Pedestrian a, Pedestrian b);
static void update_position(Pedestrian * a);

static void check_escapes();
static int is_escaped(Pedestrian * a);
static void check_flowlines(Pedestrian * a);

/*** get methods ***/
static PyObject * a_property(PyObject * self, PyObject * args);
static PyObject* get_total_count(PyObject* self);
static PyObject* get_escaped_count(PyObject* self);
static PyObject * flow_count(PyObject * self, PyObject * args);

/*** reset model ***/
static PyObject * reset_model(PyObject* self);



