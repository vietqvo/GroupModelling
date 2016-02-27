'''
Created on 13 Feb 2015

@author: quangv
'''

import sys
import os, math
from src import constants
from src import socialforce2 as force_model  # @UnresolvedImport
from src.pedestrian_types.population import PopulationGenerator
from src.simulation_observations.observations import ObservationPlots as observer_plot
from src.pygame_drawing.drawing import Canvas as image_canvas
from src.simulation_observations.pedtrack import PedTrack as ped_track
class Scenario:

    def __init__(self, parameters = {}):
        self.parameters = parameters
        
        self.timestep = constants.timestep
        self.parameters['timestep'] = self.timestep
        
        self.simulation_duration = constants.total_monitoring_duration_uni_direction
               
    def run_aggregate(self, context, simulation = True, drawing=True):
     
        self.drawing = drawing     
                                
        """ initialize social force model """
        force_model.set_parameters(self.parameters)
        
        """ initialize parameters for group members"""
        interaction_strength_mean = self.parameters["interaction_force"]
        interaction_range_mean = self.parameters["interaction_range"]
        att_strength_mean = self.parameters["attraction_force"]
        att_range_mean = self.parameters["attraction_range"]
            
        self.simulation_index = "%s" % (str(constants.myround(interaction_strength_mean)) + "_"  + 
                                   str(constants.myround(interaction_range_mean)) + "_" + 
                                   str(constants.myround(att_strength_mean)) + "_" + 
                                   str(constants.myround(att_range_mean)))  
            
        population_generator  =  PopulationGenerator(self.parameters,
                                                     context._get_group_num(), 
                                                     interaction_strength_mean,
                                                     interaction_range_mean,
                                                     att_strength_mean,
                                                     att_range_mean)         
                 
        """ perform simulation over context_placement_num"""
        radii_generators = context._get_radii_generators()
        placement_generators= context._get_placement_generators()
        
        self.avg_cohesion_degree = 0
               
          
        current_simulation_run = 0
        while current_simulation_run < len(placement_generators) :
            
            simulation_id = "%s" % (self.simulation_index + "_" + str(current_simulation_run+1))  
            print(">> running simulation %s" %(simulation_id))


            self._init_observation_plots()
            
            population_generator._generate_population(radii_generators[current_simulation_run],placement_generators[current_simulation_run])
                               
            group_pedestrians = population_generator._get_generated_group_pedestrians_population()              

            self._run(simulation_id, group_pedestrians) 
               
            self.avg_cohesion_degree += self.plots._get_cohesion_degree()
            
            """ reset force_model and increase current running time """
            force_model.reset_model()
            
            current_simulation_run+=1
        
        self.avg_cohesion_degree/=  len(placement_generators)

     
    def _init_observation_plots(self):
        self.sample_frequency = int(constants.plot_sample_frequency/self.timestep)
        self.plots = observer_plot(self.parameters)
        self.observation_plot_prefix = os.path.join(constants.observation_dir, self.parameters['name'])
           
        """ init ped track"""
        self.ped_track = ped_track()
        
    def _init_drawing(self, simulation_id):
        self.show_canvas = image_canvas(
                    self.parameters['drawing_width'],
                    self.parameters['drawing_height'],
                    self.parameters['pixel_factor'],
                    os.path.join(constants.image_dir, self.parameters['name']),
                    simulation_id)
         
    def _tick(self):
        return self._canvas("tick", constants.framerate_limit)
    
    def _canvas(self, method, *args):
        return getattr(self.show_canvas, method)(*args)
    
    def _draw(self):
        self._canvas("clear_screen")
        
        group_population_number = int(force_model.get_population_size())
        for i in range(group_population_number):
            x = force_model.group_pedestrian_a_property(i, "position")
            if math.isnan(x) ==False:
                id= force_model.group_pedestrian_a_property(i, "id")
                r = force_model.group_pedestrian_a_property(i, "radius")
                             
                if id==1.0 and int(self.time) < 20:
                    v = force_model.group_pedestrian_a_property(i,"velocity")
                    d = force_model.group_pedestrian_a_property(i,"distance")
                    
                    #v0,v_rk1,v_rk2,v_rk3,v_rk4 = force_model.group_pedestrian_a_property(i,"velocity_rk")
                    #x0,x_rk1,x_rk2,x_rk3,x_rk4 = force_model.group_pedestrian_a_property(i,"position_rk")
                    
                    
                    #self.ped_track._add_sample(self.time, v, d,
                    #                           v0,v_rk1,v_rk2,v_rk3,v_rk4,
                    #                           x0,x_rk1,x_rk2,x_rk3,x_rk4 )
                    
                self._canvas("draw_pedestrian", x,0,r,0)#pedestrian_type = 0
            else:
                print("Position is unidentified")
                sys.exit()
                                               
        self._canvas("draw_text", "t = %.2f" % self.time)
       
        self.show_canvas.update()

    def _uninit_drawing(self):
        self._canvas("quit")
    
    def _done(self,original_group_size):
       
        """ stop after 40 second period"""
        if self.time > self.simulation_duration:
            #self.plots._proceed_cut_off()
            
            """ plot save """
            #self.ped_track._save(self.observation_plot_prefix, "test")
            return True

        return False

    def _plot_sample(self):
        group_cohesion_degree = force_model.get_group_cohesion_degree()
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
                    print(">> finished at time= %.3f, frame_num= %d" % (self.time,self.frames))
                    finished = True
                
        except KeyboardInterrupt:
            pass

        if self.drawing:
            self._uninit_drawing()
   
    def _get_parameters(self):
        return self.parameters
