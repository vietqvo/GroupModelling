#include <Python.h>
#include <math.h>
#include "vector.h"

#define PI 3.14159265

typedef struct {

    double pedestrian_id; //=pedestrian Id for tracking purpose
	int group_id;
    double radius;
	
	Vector position;
	
    double in_group_a_strength; //=A
    double in_group_a_range; //=a
    double in_group_r_strength; //=R
    double in_group_r_range;//=r

    double out_group_a_strength; //A
    double out_group_a_range;//a
	double out_group_r_strength;//R
	double out_group_r_range;//r

	Vector acceleration_rk[4]; //rk for each order
	Vector position_rk[4];//rk for each order

	Vector position_temp; //this is temporary position used to calculate acceleration at each RK order
	
} Pedestrian;

/**** initial methods****/
static PyObject * add_group_pedestrian(PyObject * self, PyObject * args);//
static PyObject * set_parameters(PyObject * self, PyObject * args);//
static PyObject * update_pedestrians(PyObject * self, PyObject * args);//
static void update_position(Pedestrian * a);//
static void update_total_group_member_count(Py_ssize_t groupIndex, int count);//
static void rk_appropximate_level(int level_k, int population_count);//

static void pedestrian_from_pyobject(PyObject * o, Pedestrian * a);//
static double double_from_attribute(PyObject * o, char * name);//
static Vector vector_from_attribute(PyObject * o, char * name);//
static Vector vector_from_pyobject(PyObject * o);//


/**** update model methods ****/
static void calculate_pedestrian_repulsion_attraction(Pedestrian *a,int index, int level_rk, int population_count);//
static double calculate_magnitude_attraction_vector(Pedestrian *a, Pedestrian b,int group_type);//
static double calculate_magnitude_repulsion_vector(Pedestrian *a, Pedestrian b,int group_type);

/*** get methods ****/
static PyObject* group_pedestrian_a_property(PyObject * self, PyObject * args);//
static PyObject* get_population_size(PyObject* self);//
/*** reset model ***/
static PyObject * reset_model(PyObject* self);//
