'''
Created on 13 Feb 2015

@author: quangv
'''

import sys
import os, math
from src import constants
from src import socialforce as force_model  # @UnresolvedImport
from src.pedestrian_types.population import PopulationGenerator
from src.simulation_observations.observations import ObservationPlots as observer_plot
from src.pygame_drawing.drawing import Canvas as image_canvas
from datetime import datetime
import math as m
import numpy as np

class Scenario:

    def __init__(self, parameters = {}):
        
        self.parameters = parameters
        
        self.timestep = constants.timestep
        self.parameters['timestep'] = self.timestep
        
        self.simulation_duration = constants.total_monitoring_duration_uni_direction
         
        """ initialize social force model """
        force_model.set_parameters(self.parameters)
                       
    def run_aggregate(self,
                        in_group_a_strength, in_group_a_range,
                        in_group_r_strength, in_group_r_range,
                        out_group_a_strength, out_group_a_range, 
                        out_group_r_strength, out_group_r_range,
                        context,  
                        simulation = True,drawing=True):
     
        self.drawing = drawing                            
        total_group_num = len(self.parameters['group_num'])
        

    
        self.simulation_index = "%s" % str(datetime.now().microsecond)  
            
        population_generator  =  PopulationGenerator(self.parameters,
                                                    in_group_a_strength, in_group_a_range,
                                                    in_group_r_strength, in_group_r_range,
                                                    out_group_a_strength, out_group_a_range, 
                                                    out_group_r_strength, out_group_r_range)         
                 
        """ perform simulation over context_placement_num"""
        radii_generators = context._get_radii_generators()
        placement_generators= context._get_placement_generators()
               
        current_simulation_run = 0
        while current_simulation_run < 1: # len(placement_generators)/total_group_num :
            
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
          
            """ reset force_model and increase current running time """
            
            self.plots._save(self.observation_plot_prefix,simulation_id)
            
            force_model.reset_model()

            current_simulation_run+=1
            
            print(self.plots.get_equilibrium_time(),self.plots.get_equilibrium_cd_between_groups()/self.plots.get_equilibrium_cd_within_groups())
              
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
        
        population = []
        
        group_population_number = int(force_model.get_population_size())
        for i in range(group_population_number):
            (x,y) = force_model.group_pedestrian_a_property(i, "position")
            if math.isnan(x) ==False and math.isnan(y)==False:
                population.append([x,y])
                r = force_model.group_pedestrian_a_property(i, "radius")
                group_id = force_model.group_pedestrian_a_property(i, "groupid")
                self._canvas("draw_pedestrian", x,y,r,group_id)
            else:
                print("Position is unidentified")
                sys.exit()

        self._canvas("draw_text", "t = %.2f" % self.time)
               
        self.show_canvas.update()

    def _uninit_drawing(self):
        self._canvas("quit")
    
    def _done(self,original_group_size):
        population_number = int(force_model.get_population_size())             
        if population_number == 0 or self.time > self.simulation_duration:
            return True
        
        return False

    def _plot_sample(self):
       
        a = [[] for i in range(len(self.parameters['group_num']))]
        
        group_population_number = int(force_model.get_population_size())
        for i in range(group_population_number):
            (x,y) = force_model.group_pedestrian_a_property(i, "position")
            r = force_model.group_pedestrian_a_property(i, "radius")
            group_id = force_model.group_pedestrian_a_property(i, "groupid")
            a[int(group_id)].append((x, y, r, group_id))
      
        ## compute cd_distance_inside groups
        comfortable_distances_within_group = self.compute_cd_inside_group(a) 
        comfortable_distances_between_groups = self.compute_cd_between_groups(a)
       
        self.plots._add_sample(int(self.time), comfortable_distances_within_group, comfortable_distances_between_groups)
        
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
                    finished = True
                
        except KeyboardInterrupt:
            pass

        if self.drawing:
            self._uninit_drawing()
        
    def _get_parameters(self):
        return self.parameters

    def _get_simulation_index(self):
        return self.simulation_index   
    
    def _distance(self, x1, y1, r1, x2, y2, r2):
        a = m.sqrt(m.pow(x1 - x2, 2) + m.pow(y1 - y2, 2))
        a = a - (r1 + r2)
        return a
    
    def compute_cd_inside_group(self,a):
        
        comfortable_distances_within_group_py = []
        for i in range(len(a)):
            b = [[] for f in range(len(a[i]))]
            
            for k in range(len(a[i])):                
                for l in range (len(a[i])):
                    if k == l:
                        b[k].append(0)
                    else:
                        b[k].append(self._distance(a[i][k][0], a[i][k][1], a[i][k][2], a[i][l][0], a[i][l][1], a[i][l][2]))
            
            cd_inside_group = []
            for k in range(len(b)):
                temp = b[k]
                while 0 in temp: temp.remove(0)
                cd_inside_group.append(np.mean(temp))
            
            comfortable_distances_within_group_py.append(np.mean(cd_inside_group))     
               
        return comfortable_distances_within_group_py
    
    def compute_cd_between_groups(self, a):
        
        cd_between_groups = []
        
        for i in range(len(a)):
            for j in range(i+1,len(a)):
                
                for ped_index in range(len(a[i])):
                    b = []
                    for ped_index2 in range(len(a[j])):
                        b.append(self._distance(a[i][ped_index][0], a[i][ped_index][1], a[i][ped_index][2],
                                                a[j][ped_index2][0], a[j][ped_index2][1], a[j][ped_index2][2]))
                    
                    
                    cd_between_groups.append(np.mean(b))                                                                                          
        
        return np.mean(cd_between_groups)        
    