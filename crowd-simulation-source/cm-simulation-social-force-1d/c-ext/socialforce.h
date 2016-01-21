#include <Python.h>
#include <math.h>

typedef struct {
    double radius;
    double time; //traveling duration from initial pos to current pos
    double initial_desired_velocity;
    double force_unit; //=A
    double p_type; //=pedestrian type
    double pedestrian_id; //=pedestrian Id for tracking purpose

    double position;
    double target;

    double velocity;
    double acceleration;

    double desired_force_tracking; //this is only for tracking purpose
    double interaction_force_tracking; //this is only for tracking purpose

} Pedestrian;

/**** initial methods****/
static PyObject * add_pedestrian(PyObject * self, PyObject * args);
static PyObject * set_parameters(PyObject * self, PyObject * args);
static PyObject * update_pedestrians(PyObject * self, PyObject * args);
static void update_total_count(Py_ssize_t count);

static void pedestrian_from_pyobject(PyObject * o, Pedestrian * a);
static double double_from_attribute(PyObject * o, char * name);

/**** update model methods ****/
static void calculate_desired_acceleration(Pedestrian * a);
static void calculate_pedestrian_repulsion(int index);

static void update_position(Pedestrian * a);
static void check_escapes();
static int is_escaped(Pedestrian * a);

/*** get methods ****/
static PyObject* a_property(PyObject * self, PyObject * args);
static PyObject* get_population_size(PyObject* self);
static PyObject* get_escaped_num(PyObject* self);
static PyObject* check_escaped(PyObject * self, PyObject * args);


/*** reset model ***/
static PyObject * reset_model(PyObject* self);
