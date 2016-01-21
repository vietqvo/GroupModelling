'''
Created on 13 Feb 2015

@author: quangv
'''

import sys
import os, math
from datetime import datetime
import csv
import json
from src import constants
from src import socialforce as force_model  # @UnresolvedImport
from src.pedestrian_types.population import PopulationGenerator
from src.simulation_observations.observations import ObservationPlots as observer_plot
from src.pygame_drawing.drawing import Canvas as image_canvas

class Scenario:

    def __init__(self, parameters = {}):
        self.parameters = parameters
        
        self.timestep = constants.timestep
        self.parameters['timestep'] = self.timestep
    
        self.simulation_duration = constants.total_monitoring_duration_bi_direction
                 
    def run_aggregate(self,
                      simulation_num, 
                      parameter_distribution_plot =True,
                      simulation = True,
                      drawing=True, 
                      observation_plot=True,
                      simulation_recording=True,
                      log_generation=True):
     
        self.drawing = drawing     
        self.parameter_plot = parameter_distribution_plot                            
        self.observation_plot = observation_plot     
    
        self.simulation_recording = simulation_recording
        self.log_generation = log_generation
               
        escape_rates_prototype_average = []

        #initialize social force model
        force_model.set_parameters(self.parameters)
        
        analysis_file = open( "%s.csv" % os.path.join(constants.analysis_dir, "parameter"), "w",newline='')
        writer = csv.writer(analysis_file,delimiter=',')
        writer.writerow(["SimulationId","Naverage","Taverage","Bottleneck"])
        
        if self.parameter_plot == True:
            self._init_quantification_plots()
          
        strTime = "%s" % (datetime.now().microsecond);
  
        self.population_generator  =  PopulationGenerator(self.parameters, self.parameters['average_num'], self.parameter_plot, strTime)         
        
        escape_rates_prototype_average.clear()    
        current_simulation_run = 0
        
        while current_simulation_run < simulation_num and simulation==True:
                
            simulation_id = "%s" % (strTime + "_" + str(current_simulation_run+1))
            print("Simulation Id=%s" % simulation_id)
                
            self._init_observation_plots()
            
            self.bottleneck_info =[]
            self.bottleneck_info.clear()
            
            """ initialize random pedestrian placements""" 
            pedestrians= self.population_generator._generate_population(self.parameters['start_areas'],self.log_generation)                 
            
            if self.log_generation:
                self.population_generator._log_generation(os.path.join(constants.log_dir, simulation_id))
                        
            print(">>> Simulation time=%d: Prototype=%s - Ped_num=%d- scenario=%s " %(current_simulation_run+1, "average",len(pedestrians),self.parameters['name']))  
            self._run(simulation_id, pedestrians) 

            """ plot observations """
            if self.observation_plot:    
                self.plots._save(self.observation_plot_prefix,simulation_id)
                        
                """ write SimulationId,escape_num_different_prototype,escape_num_average_prototype,last_escapetime_different_prototype,last_escapetime_average_prototype"""    
                writer.writerow((simulation_id,
                                        self.plots._get_escaped_num_average_prototype(),
                                        self.plots._get_last_escape_time_average_prototype(), json.dumps(self.bottleneck_info)))
    
            """reset force_model and increase current running time """
            force_model.reset_model()
            current_simulation_run +=1
    
        analysis_file.close()
          
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
        population_number = int(force_model.get_population_size())
        for i in range(population_number):
            x = force_model.a_property(i, "position")
            if math.isnan(x) ==False:
                self._canvas("draw_pedestrian", x)

            else:
                print("Position is unidentified")
                sys.exit()
        self._canvas("draw_text", "t = %.2f" % self.time)
        
        for t in self.parameters['targets']:
            self._canvas("draw_target", t)
       
        for s in self.parameters['start_areas']:
            self._canvas("draw_start_area", s)
        
        self.show_canvas.update()

    def _uninit_drawing(self):
        self._canvas("quit")
    
    def _done(self):
        population_number = int(force_model.get_population_size())
        if population_number == 0 or self.time > self.simulation_duration:
            return True
        
        return False

    def _plot_sample(self):
        escaped_number = int(force_model.get_escaped_num())            
        self.plots._add_sample(int(self.time), escaped_number)
             
        is_bottle_neck = int(force_model.is_bottle_neck()) 
        if is_bottle_neck==1:
            self.bottleneck_info.clear()
            population_number = int(force_model.get_population_size())
            for i in range(population_number):
                self.bottleneck_info.append(dict(
                    position = force_model.a_property(i, "position"),
                    id = force_model.a_property(i, "id"),
                    velocity =force_model.a_property(i, "velocity"),
                    initial_position =  force_model.a_property(i, "initial_position"),
                    desired_force_tracking = force_model.a_property(i, "desired_force_tracking"),           
                    initial_desired_velocity = force_model.a_property(i, "initial_desired_velocity"),           
                    force_unit = force_model.a_property(i, "force_unit"),  
                    interaction_force_tracking = force_model.a_property(i, "interaction_force_tracking"),  
            
                    time_travelled = force_model.a_property(i, "time_travelled"),  
                    distance_travelled = force_model.a_property(i, "distance_travelled")))
              
    def _run(self, simulation_id, pedestrian_population):
      
        self.time = 0.0
        self.frames = 0
        
        if pedestrian_population is not None and len(pedestrian_population)>0:
            for pedestrian in  pedestrian_population:          
                force_model.add_pedestrian(pedestrian)
                
        self._init_drawing(simulation_id)
               
        finished = False
        try:
            while self._tick() and not finished:
                force_model.update_pedestrians()
               
                if self.drawing: 
                    self._draw()
                
                if self.observation_plot and not self.frames % self.sample_frequency:
                    self._plot_sample()
          
                self.time += self.timestep
                self.frames += 1

                if self._done():
                    self._plot_sample()
                    print(">>>>> finished at time= %.3f, frame_num= %d" % (self.time,self.frames))
                    finished = True
                
        except KeyboardInterrupt:
            pass

        if self.drawing:
            self._uninit_drawing()
    