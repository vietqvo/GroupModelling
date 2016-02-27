'''
Created on 13 Feb 2015

@author: quangv
'''

import sys
import os, math, csv
from src import constants
from src import socialforce as force_model  # @UnresolvedImport
from src.pedestrian_types.population import PopulationGenerator
from src.simulation_observations.observations import ObservationPlots as observer_plot
from src.pygame_drawing.drawing import Canvas as image_canvas
from datetime import datetime

class Scenario:

    def __init__(self, parameters = {}):
        
        self.parameters = parameters
        
        self.timestep = constants.timestep
        self.parameters['timestep'] = self.timestep
        
        self.simulation_duration = constants.total_monitoring_duration_uni_direction
                       
    def run_aggregate(self,
                      total_group_num,
                      v_param, re_param,
                      rep_s_param, rep_ra_param,
                      att_s_param, att_ra_param,
                      att_force_param,att_interaction_param,
                      context,  
                      simulation = True,
                      drawing=True):
     
        self.drawing = drawing                            
        
        """ initialize social force model """
        force_model.set_parameters(self.parameters)
    
        self.simulation_index = "%s" % str(datetime.now().microsecond)  
            
        population_generator  =  PopulationGenerator(self.parameters,
                                                     total_group_num,
                                                     v_param, re_param, 
                                                     rep_s_param,rep_ra_param,
                                                     att_s_param,att_ra_param,
                                                     att_force_param,att_interaction_param)         
                 
        """ perform simulation over context_placement_num"""
        radii_generators = context._get_radii_generators()
        placement_generators= context._get_placement_generators()
        
        self.avg_cohesion_degree = [0] *  total_group_num
        self.avg_flow_rate = [0] * total_group_num
        self.avg_overal_flow_rate = 0
               
        """ add average result log through 10 times"""       
        analysis_file = open( "%s.csv" % os.path.join(constants.analysis_dir, self.simulation_index), "w", newline='')
        writer = csv.writer(analysis_file,delimiter=',')
        log_title = constants._generate_log_title(self.parameters['group_id'])         
        writer.writerow(log_title)
        
        
        current_simulation_run = 0
        while current_simulation_run < len(placement_generators)/total_group_num :
            
            simulation_id = "%s" % (self.simulation_index + "_" + str(current_simulation_run+1))  
            print(">> running simulation %s" %(simulation_id))
            current_record = []
            current_record.append(simulation_id)
            
            self._init_observation_plots(total_group_num)
            
            index = current_simulation_run*total_group_num
            radii_generator = radii_generators[index:index + total_group_num]
            placement_generator = placement_generators[index:index + total_group_num]
            
            population_generator._generate_population(radii_generator,placement_generator)  
                    
            group_pedestrians = population_generator._get_generated_group_pedestrians_population()              

            self._run(simulation_id, group_pedestrians) 
            
            #extract cohesion degree of each group after remove 10 seconds
            cohesion_degrees = self.plots._get_cohesion_degree()
            for i in range(len(self.avg_cohesion_degree)):
                self.avg_cohesion_degree[i] += cohesion_degrees[i]
                current_record.append(cohesion_degrees[i])
                    
            #flow rate of each group of last escape,
            overal_flowrate = 0
            flow_rates = self.plots._get_flow_rate()
            for i in range(len(self.avg_flow_rate)):
                self.avg_flow_rate[i] += flow_rates[i]
                overal_flowrate +=flow_rates[i]
                current_record.append(flow_rates[i])
            
            #overall flow rate of last escape
            overal_flowrate/=total_group_num
            current_record.append(overal_flowrate)
                  
            self.avg_overal_flow_rate += overal_flowrate
            
            
            """ reset force_model and increase current running time """
            writer.writerow((current_record))
            force_model.reset_model()
            self.plots.reset_sample()
            
            current_simulation_run+=1
        
        analysis_file.close()
        
        for i in range(total_group_num):
            self.avg_cohesion_degree[i]/=  len(placement_generators)
            self.avg_flow_rate[i] /=  len(placement_generators)
        
        self.avg_overal_flow_rate/=len(placement_generators)
        
        print("c_d") 
        print(self.avg_cohesion_degree)
        
        print("f_r")
        print(self.avg_flow_rate)
        
        print("overal_flowrate")
        print(self.avg_overal_flow_rate)
              
    def _init_observation_plots(self,total_group_num):
        self.sample_frequency = int(constants.plot_sample_frequency/self.timestep)
        self.plots = observer_plot(self.parameters,total_group_num)
        self.observation_plot_prefix = os.path.join(constants.observation_dir, self.parameters['name'])
           
    def _init_drawing(self, simulation_id):
        self.show_canvas = image_canvas(
                    self.parameters['drawing_width'],
                    self.parameters['drawing_height'],
                    self.parameters['pixel_factor'])
         
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
                group_id = force_model.group_pedestrian_a_property(i, "groupid")
                self._canvas("draw_pedestrian", x,y,r,group_id)
            else:
                print("Position is unidentified")
                sys.exit()
                                        
        self._canvas("draw_text", "t = %.2f" % self.time)
        
        for t in self.parameters['targets']:
            self._canvas("draw_target", *t)
       
        for w in self.parameters['walls']:
            self._canvas("draw_wall", w)
       
        self.show_canvas.update()

    def _uninit_drawing(self):
        self._canvas("quit")
    
    def _done(self,original_group_size):
        population_number = int(force_model.get_population_size())     

        if population_number == 0 or self.time > self.simulation_duration: 
            self.plots._proceed_cut_off()
            return True
        
        return False

    def _plot_sample(self):
        group_cohesion_degree = force_model.get_group_cohesion_degree()
        escaped_number = force_model.get_group_escaped_num()
        #print(group_cohesion_degree)
        #print(escaped_number)
        
        self.plots._add_sample(int(self.time), group_cohesion_degree, escaped_number)
        
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
        
    def _get_avg_cohesion_degree(self):
        return self.avg_cohesion_degree

    def _get_simulation_index(self):
        return self.simulation_index   