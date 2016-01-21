'''
Created on 13 Feb 2015

@author: quangv
'''
import constants
import sys
from population import PopulationGenerator
import nomadmodel as nomad_model
from drawing import Canvas as image_canvas
from observations import ObservationPlots as observer_plot

import os, math
from datetime import datetime

class Scenario:
   
    def __init__(self, parameters = {}):
        self.parameters = parameters
        
        self.parameters["flowrate_lines"] = [self.parameters["flowrate_line"]] 

        self.timestep = constants.timestep
        self.parameters['timestep'] = self.timestep
        
        self.time = 0
        
        self.population_generator  =  PopulationGenerator(self.parameters)     
                          
        self.drawing = True
        self.create_observation_plot = False
        self.create_quantification_plots = False
                                    
    def run(self):
        
        if self.create_quantification_plots == True:
            self._init_quantification_plots()
       
        if self.create_observation_plot ==True:
            self._init_observation_plots()
        
        #nomad model init
        nomad_model.set_parameters(self.parameters)
        
        #population prototypes init
        self.population_generator._generate_population(self.parameters['start_areas'], self.parameters['young_num'],self.parameters['adult_num'],self.parameters['elderly_num'],self.create_quantification_plots)
        
        #run prototype P1
        pedestrians = self.population_generator._get_pedestrian_type_population()  
        self._run(pedestrians) 
        
        #nomad model reset        
        nomad_model.reset_model()

        #run prototype P2
        average_pedestrians =  self.population_generator._get_averaged_pedestrians()       
        self._run(average_pedestrians) 
        
    def _init_quantification_plots(self):
        self.quantification_plot_prefix = os.path.join(constants.quantification_plot_dir, self.parameters['name'])
        self.parameters['quantification_plot_prefix'] = self.quantification_plot_prefix
     
    def _init_observation_plots(self):
        self.sample_frequency = int(constants.plot_sample_frequency/self.timestep)
        self.plots = observer_plot(self.sample_frequency, self.parameters)
        self.observation_plot_prefix = os.path.join(constants.observation_plot_dir, self.parameters['name'])
          
    def _init_drawing(self):
        self.show_canvas = image_canvas(
                    self.parameters['drawing_width'],
                    self.parameters['drawing_height'],
                    self.parameters['pixel_factor'],
                    os.path.join(constants.image_dir, self.parameters['name']))
          
    def _tick(self):
        return self._canvas("tick", constants.framerate_limit)
    
    def _canvas(self, method, *args):
        return getattr(self.show_canvas, method)(*args)
    
    def _draw(self):
        self._canvas("clear_screen")
        
        population_number = int(nomad_model.get_total_count())
        for i in range(population_number):
            (x,y) = nomad_model.a_property(i, "position")
            if math.isnan(x) ==False and math.isnan(y)==False:
                r = nomad_model.a_property(i, "radius")
                t = nomad_model.a_property(i, "p_type")
                self._canvas("draw_pedestrian", x,y,r,t)
            else:
                print("Position is unidentified")
                sys.exit()
        self._canvas("draw_text", "t = %.2f" % self.time)
        
        for t in self.parameters['targets']:
            self._canvas("draw_target", *t)
        
        for s in self.parameters['start_areas']:
            self._canvas("draw_start_area", s)
            
        self.show_canvas.update()
 
    def _uninit_drawing(self):
        self._canvas("quit")
    
    def _done(self):
        population_number = int(nomad_model.get_total_count())
        if population_number == 0:
            return True
        if self.time > constants.total_monitoring_duration:
            return True
        
        return False

    def _plot_sample(self):
        population_number = int(nomad_model.get_total_count())
        if population_number == 0:
            return  
        flowrates = []
        for i in range(len(self.parameters["flowrate_lines"])):
            (x1,y1,x2,y2) = self.parameters["flowrate_lines"][i]
            flow_length = math.sqrt((x2-x1)**2+(y2-y1)**2)
            flow_count = nomad_model.flow_count(i)
            flowrate = flow_count/constants.plot_sample_frequency/flow_length
            flowrates.append(flowrate)

        self.plots.add_sample(self.time, 
                flowrate=flowrates)
    
    def _writeNumEscaped(self):
        escaped_number = int(nomad_model.get_escaped_count())
        print("time %d: num %d "  % (int(self.time), escaped_number))
              
    def _run(self, pedestrian_population):
        
        self.time = 0.0
        self.frames = 0
        
        if pedestrian_population is not None and len(pedestrian_population)>0:
            for pedestrian in  pedestrian_population:
                nomad_model.add_pedestrian(pedestrian)
                
        if self.drawing:
            self._init_drawing()

        success = False
        lastObservered = 0
        
        try:
            while self._tick():
                nomad_model.update_pedestrians()
             
                if self.drawing: 
                    self._draw()
                    
                if self.create_observation_plot and not self.frames % self.sample_frequency:
                    self._plot_sample()
    
                observeredTime = int(self.time)
                if observeredTime in constants.observation_range and observeredTime-lastObservered > 10:
                    self._writeNumEscaped()
                    lastObservered = observeredTime
                
                self.time += self.timestep
                self.frames += 1

                if self._done():
                    success = True
                    self._writeNumEscaped()
                    break
        except KeyboardInterrupt:
            pass
        print

        if self.drawing:
            self._uninit_drawing()
        
        if self.create_observation_plot:
            currentTime=datetime.now()
            strTime = "%s" % (currentTime.microsecond);
            self.plots.save(self.observation_plot_prefix,strTime)
                
        return success
