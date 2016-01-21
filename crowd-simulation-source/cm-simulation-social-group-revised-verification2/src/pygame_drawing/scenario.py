'''
Created on 13 Feb 2015

@author: quangv
'''

import sys
import os, math, csv
from src import constants
#from src import socialforce as force_model  # @UnresolvedImport
from src import socialforce2 as force_model  # @UnresolvedImport
from src.pedestrian_types.population import PopulationGenerator
from src.simulation_observations.observations import ObservationPlots as observer_plot
from src.pygame_drawing.drawing import Canvas as image_canvas

class Scenario:

    def __init__(self, parameters = {}):
        self.parameters = parameters
        
        self.timestep = constants.timestep
        self.parameters['timestep'] = self.timestep
        
        if len(self.parameters['start_areas']) ==1:
            self.simulation_duration = constants.total_monitoring_duration_uni_direction
        else:
            self.simulation_duration = constants.total_monitoring_duration_bi_direction
                       
    def run_aggregate(self,
                      velocity_param,
                      relax_param,
                      strength_param,
                      range_param,
                      att_s_param,
                      att_ra_param,
                      context,  
                      parameter_distribution_plot =True,
                      simulation = True,
                      drawing=True,
                      rep=False):
     
        self.drawing = drawing     
        self.parameter_plot = parameter_distribution_plot                            
        
        """ initialize social force model """
        force_model.set_parameters(self.parameters)
        
        """ initialize parameters for group members"""
        if rep == False:
            velocity_mean = self.parameters["velocity_mean"][0] + velocity_param * self.parameters["velocity_step"]
            relaxation_mean = self.parameters["relaxation_mean"][0] + relax_param * self.parameters["relaxation_step"]
            interaction_strength_mean = self.parameters["interaction_force"][0] + strength_param * self.parameters["interaction_force_step"]
            interaction_range_mean = self.parameters["interaction_range"][0] + range_param * self.parameters["interaction_range_step"]
            att_strength_mean = self.parameters["attraction_force"][0] + range_param * self.parameters["attraction_force_step"]
            att_range_mean = self.parameters["attraction_range"][0] + range_param * self.parameters["attraction_range_step"]
            
        else:
            velocity_mean = velocity_param
            relaxation_mean = relax_param
            interaction_strength_mean = strength_param
            interaction_range_mean = range_param
            att_strength_mean = att_s_param
            att_range_mean = att_ra_param
      
        self.simulation_index = "%s" % (str(constants.myround(velocity_mean)) + "_" + 
                                   str(constants.myround(relaxation_mean)) + "_" + 
                                   str(constants.myround(interaction_strength_mean)) + "_"  + 
                                   str(constants.myround(interaction_range_mean)) + "_" + 
                                   str(constants.myround(att_strength_mean)) + "_" + 
                                   str(constants.myround(att_range_mean)))  
            
        population_generator  =  PopulationGenerator(self.parameters,
                                                     self.parameters['group_num'], 
                                                     velocity_mean,
                                                     relaxation_mean,
                                                     interaction_strength_mean,
                                                     interaction_range_mean,
                                                     att_strength_mean,
                                                     att_range_mean)         
                 
        """ perform simulation over context_placement_num"""
        radii_generators = context._get_radii_generators()
        placement_generators= context._get_placement_generators()
        
        self.avg_cohesion_degree = 0
               
        """ add sub log file and average scalar value through 10 times"""       
        analysis_file = open( "%s.csv" % os.path.join(constants.analysis_dir, self.simulation_index), "w", newline='')
        writer = csv.writer(analysis_file,delimiter=',')
        writer.writerow(["SimulationId","cohesion_degree"])
        
        current_simulation_run = 0
        while current_simulation_run < len(placement_generators) :
            
            simulation_id = "%s" % (self.simulation_index + "_" + str(current_simulation_run+1))  
            print(">> running simulation %s" %(simulation_id))
            
            if self.parameter_plot == True:
                self._init_quantification_plots()

            self._init_observation_plots()
            
            population_generator._generate_population(radii_generators[current_simulation_run],placement_generators[current_simulation_run])
            
            """ log dump"""    
            population_generator._log_generation(os.path.join(constants.log_dir, simulation_id))
                    
            """ get in-group pedestrians """ 
            group_pedestrians = population_generator._get_generated_group_pedestrians_population()              

            self._run(simulation_id, group_pedestrians) 
            
            writer.writerow((simulation_id,self.plots._get_cohesion_degree_str()))
             
            # REMEMBER TO CHECK NAN, ASSIGN 0
            if math.isnan(self.plots._get_cohesion_degree()) == False:
                self.avg_cohesion_degree += self.plots._get_cohesion_degree()
            else:
                self.avg_cohesion_degree += 0
            
            """ reset force_model and increase current running time """
            force_model.reset_model()
            
            current_simulation_run+=1
        
        analysis_file.close()
        
        self.avg_cohesion_degree/=  len(placement_generators)
        
        if rep == True:
            print("cohesion degree: %.3f" % (self.avg_cohesion_degree))
            
    def _init_quantification_plots(self):
        self.quantification_plot_prefix = os.path.join(constants.parameter_distribution_dir, self.parameters['name'])
        self.parameters['quantification_plot_prefix'] = self.quantification_plot_prefix
     
    def _init_observation_plots(self):
        self.sample_frequency = int(constants.plot_sample_frequency/self.timestep)
        self.plots = observer_plot(self.parameters)
        self.observation_plot_prefix = os.path.join(constants.observation_dir, self.parameters['name'])
           
    def _init_drawing(self, simulation_id):
        self.show_canvas = image_canvas(
                    self.parameters['drawing_width'],
                    self.parameters['drawing_height'],
                    self.parameters['pixel_factor'],
                    os.path.join(constants.image_dir, self.parameters['name']),
                    os.path.join(constants.video_dir, self.parameters['name']),
                    simulation_id)
         
    def _tick(self):
        return self._canvas("tick", constants.framerate_limit)
    
    def _canvas(self, method, *args):
        return getattr(self.show_canvas, method)(*args)
    
    def _draw(self):
        self._canvas("clear_screen")
        
        group_population_number = int(force_model.get_population_size())
        for i in range(group_population_number):
            (x,y) = force_model.group_pedestrian_a_property(i, "position")
            if math.isnan(x) ==False and math.isnan(y)==False:
                r = force_model.group_pedestrian_a_property(i, "radius")
                t = force_model.group_pedestrian_a_property(i, "p_type")
                               
                self._canvas("draw_pedestrian", x,y,r,t)
            else:
                print("Position is unidentified")
                sys.exit()
        
        (group_center_x,group_center_y) = force_model.get_group_centre_of_mass()
        #print( (group_center_x,group_center_y))
        self._canvas("draw_group_center", group_center_x,group_center_y)
                                        
        self._canvas("draw_text", "t = %.2f" % self.time)
       
        for s in self.parameters['start_areas']:
            self._canvas("draw_start_area", s)
        
        self.show_canvas.update()

    def _uninit_drawing(self):
        self._canvas("quit")
    
    def _done(self,original_group_size):
       
        #"""stop when one pedestrian in group left"""
        #if population_number < original_group_size or self.time > self.simulation_duration: 
        #    self.plots._proceed_cut_off()
        #    return True
        """ stop after 50 second period"""
        if self.time > self.simulation_duration:
            self.plots._proceed_cut_off() #remover 10 second period
            return True

        return False

    def _plot_sample(self):
        group_cohesion_degree = force_model.get_group_cohesion_degree()
        #print(group_cohesion_degree)
        self.plots._add_sample(int(self.time), group_cohesion_degree)
        
    def _run(self, simulation_id, group_pedestrians): 
      
        self.time = 0.0
        self.frames = 0
        group_size =len (group_pedestrians)
        if group_pedestrians is not None and len(group_pedestrians)>0:
            for group_member in  group_pedestrians:                
                force_model.add_group_pedestrian(group_member)
                        
        self._init_drawing(simulation_id)
               
        finished = False
        try:
            while self._tick() and not finished:
                force_model.update_pedestrians()
               
                if self.drawing: 
                    self._draw()
                
                if not self.frames % self.sample_frequency:
                    self._plot_sample()
          
                self.time += self.timestep
                self.frames += 1

                if self._done(group_size):
                    #self._plot_sample()
                    print(">> finished at time= %.3f, frame_num= %d" % (self.time,self.frames))
                    finished = True
                
        except KeyboardInterrupt:
            pass

        if self.drawing:
            self._uninit_drawing()
    
    def _get_velocity_vary_step(self):
        return (self.parameters['velocity_mean'][1] - 
                self.parameters['velocity_mean'][0]) / self.parameters['velocity_step']
          
    def _get_relax_vary_step(self):
        return (self.parameters['relaxation_mean'][1] - 
                self.parameters['relaxation_mean'][0]) / self.parameters['relaxation_step']
   
  
  
    def _get_strength_vary_step(self):
        return (self.parameters['interaction_force'][1] - 
                self.parameters['interaction_force'][0]) / self.parameters['interaction_force_step']
    
    def _get_range_vary_step(self):
        return (self.parameters['interaction_range'][1] - 
                self.parameters['interaction_range'][0]) / self.parameters['interaction_range_step']
   
    def _get_attraction_strength_vary_step(self):
        return (self.parameters['attraction_force'][1] - 
                self.parameters['attraction_force'][0]) / self.parameters['attraction_force_step']
                   
    def _get_attraction_range_vary_step(self):
        return (self.parameters['attraction_range'][1] - 
                self.parameters['attraction_range'][0]) / self.parameters['attraction_range_step']
    
    def _get_parameters(self):
        return self.parameters
        
    def _get_avg_cohesion_degree(self):
        return self.avg_cohesion_degree
        
    def _get_simulation_index(self):
        return self.simulation_index   