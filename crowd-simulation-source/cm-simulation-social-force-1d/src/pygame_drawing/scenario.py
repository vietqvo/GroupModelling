'''
Created on 13 Feb 2015

@author: quangv
'''

import sys
import os, math
from datetime import datetime
import csv

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
                      sample_num, 
                      simulation_num, 
                      distribution_average_prototype = "normal",
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
        
        current_population_regeneration_run = 0
        
        escape_rates_prototype_different = []
        escape_rates_prototype_average = []

        #initialize social force model
        force_model.set_parameters(self.parameters)
        
        analysis_file = open( "%s.csv" % os.path.join(constants.analysis_dir, "parameter"), "w",newline='')
        writer = csv.writer(analysis_file,delimiter=',')
        writer.writerow(["SimulationId","Ndifference","Naverage","Tdifference","Taverage"])
        
        while current_population_regeneration_run < sample_num:
            if self.parameter_plot == True:
                self._init_quantification_plots()
          
            currentTime =datetime.now()
            strTime = "%s" % (currentTime.microsecond);
            print("Sampling Id=%s" % strTime)      
            self.population_generator  =  PopulationGenerator(self.parameters,
                                                              self.parameters['young_num'], 
                                                              self.parameters['elderly_num'],
                                                              distribution_average_prototype,
                                                              self.parameter_plot,
                                                              strTime)         
            
            current_simulation_run = 0
            escape_rates_prototype_different.clear()
            escape_rates_prototype_average.clear()
                    
            while current_simulation_run < simulation_num and simulation==True:
                
                simulation_id = "%s" % (strTime + "_" + str(current_simulation_run+1))
                print("Simulation Id=%s" % simulation_id)
                
                self._init_observation_plots()
                
                """ initialize random radii and pedestrian placements""" 
                is_succeed = self.population_generator._generate_population(self.parameters['start_areas'],self.log_generation)
                
                if is_succeed == True:
                    """ check for log dump"""
                    
                    if self.log_generation:
                        self.population_generator._log_generation(os.path.join(constants.log_dir, simulation_id))
                        
                    """ run the prototype of different distribution - it's type is 1 """ 
                    pedestrians = self.population_generator._get_different_pedestrians_population()               
                    print(">>> Sample time=%d: Simulation time=%d: Prototype=%d - Ped_num=%d- scenario=%s " %(current_population_regeneration_run+1, current_simulation_run+1, 1,len(pedestrians),self.parameters['name']))  
                    self._run(simulation_id, 1, pedestrians) 
                        
                    """  reset social force model """         
                    force_model.reset_model()
            
                    """ run the prototype of average  distribution - it's type is 2 """
                    average_pedestrians =  self.population_generator._get_averaged_pedestrians_population()
                    print(">>> Sample time=%d: Simulation time=%d, Prototype=%d - Ped_num=%d- scenario=%s" %(current_population_regeneration_run+1, current_simulation_run+1,2,len(average_pedestrians),self.parameters['name']))         
                    self._run(simulation_id, 2, average_pedestrians)       
            
                    """ plot observations """
                    if self.observation_plot:    
                        self.plots._save(self.observation_plot_prefix,simulation_id)
                        
                        """ write SimulationId,escape_num_different_prototype,escape_num_average_prototype,last_escapetime_different_prototype,last_escapetime_average_prototype""" 
                        writer.writerow((simulation_id,
                                        self.plots._get_escaped_num_different_distribution_prototype(),
                                        self.plots._get_escaped_num_average_prototype(),
                                        self.plots._get_last_escape_time_different_distribution_protype(),
                                        self.plots._get_last_escape_time_average_prototype()))
    
                    """ reset force_model and increase current running time """
                    force_model.reset_model()
                    current_simulation_run +=1
            
            current_population_regeneration_run +=1
        
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
                r = force_model.a_property(i, "radius")
                t = force_model.a_property(i, "p_type")
                self._canvas("draw_pedestrian", x,r,t)
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

    def _plot_sample(self, prototype):
        escaped_number = int(force_model.get_escaped_num())  
            
        self.plots._add_sample(prototype, int(self.time), escaped_number)
        
    def _run(self, simulation_id, prototype, pedestrian_population):
      
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
                    self._plot_sample(prototype)
          
                self.time += self.timestep
                self.frames += 1

                if self._done():
                    self._plot_sample(prototype)
                    print(">>>>> finished at time= %.3f, frame_num= %d" % (self.time,self.frames))
                    finished = True
                
        except KeyboardInterrupt:
            pass

        if self.drawing:
            self._uninit_drawing()
    