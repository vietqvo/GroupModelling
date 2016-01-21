#include <Python.h>
#include <math.h>
#include "vector.h"

#define ESCAPE_THRESHOLD 50

typedef struct {
    double radius;
    double time; //traveling duration from initial pos to current pos
    double initial_desired_velocity;
    double max_velocity;
    double relax_time;
    double force_unit; //=A
    double interaction_range; //=B
    double interaction_lamda; //=lambda
    double p_type; //=pedestrian type
    double pedestrian_id; //=pedestrian Id for tracking purpose
    Vector desired_velocity; //illustrate desired_speed at time t on desired direction
    double impatience_level;//illustrate panic at time t


    Vector position;
    Vector initial_position;
    Vector target;
    Vector velocity;
    Vector acceleration;

    Vector desired_force_tracking; //this is only for tracking purpose
    Vector interaction_force_tracking; //this is only for tracking purpose
    Vector obstacle_force_tracking;//this is only for tracking purpose

} Pedestrian;

typedef struct {
    Vector start;
    Vector end;
    double length;
} Wall;

/**** initial methods****/
static PyObject * add_pedestrian(PyObject * self, PyObject * args);
static PyObject * set_parameters(PyObject * self, PyObject * args);
static PyObject * update_pedestrians(PyObject * self, PyObject * args);
static void update_total_count(Py_ssize_t count);

static void pedestrian_from_pyobject(PyObject * o, Pedestrian * a);
static double double_from_attribute(PyObject * o, char * name);
static Vector vector_from_attribute(PyObject * o, char * name);

static Wall wall_from_pyobject(PyObject *o);
static Vector vector_from_pyobject(PyObject * o);
static void init_walls(PyObject * p_walls, Wall * walls_p, Py_ssize_t w_count);


/**** update model methods ****/
static void calculate_desired_acceleration(Pedestrian * a);
static void calculate_pedestrian_repulsion(int index);
static void calculate_wall_repulsion(Pedestrian * a);
static int find_repulsion_points(Pedestrian * a, Vector repulsion_points[]);
static Vector calculate_repulsion_vector(Pedestrian a, Pedestrian b);
static Vector calculate_wall_repulsion_point(Pedestrian * a, Vector repulsion_point);
static void update_position(Pedestrian * a);
static void check_escapes();
static int is_escaped(Pedestrian * a);

/*** get methods ****/
static PyObject* a_property(PyObject * self, PyObject * args);
static PyObject* get_population_size(PyObject* self);
static PyObject* get_escaped_num(PyObject* self);
static PyObject* check_escaped(PyObject * self, PyObject * args);

static PyObject* get_total_panic_level(PyObject* self);
static PyObject* get_total_interaction_force(PyObject* self);

/*** reset model ***/
static PyObject * reset_model(PyObject* self);



