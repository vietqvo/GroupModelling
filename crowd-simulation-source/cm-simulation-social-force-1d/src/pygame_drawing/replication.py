'''
Created on 23 Apr 2015

@author: quangv
'''
import sys
import os, math
import json
import random

from src import constants # @UnresolvedImport
from src import socialforce as force_model  # @UnresolvedImport
from src.simulation_observations.observations import ObservationPlots as observer_plot # @UnresolvedImport
from src.pygame_drawing.drawing import Canvas as image_canvas # @UnresolvedImport
from src.pedestrian_types.population_log import PopulationLog as population_log # @UnresolvedImport
from src.pedestrian_types.population_log import PopulationLog_Decoder # @UnresolvedImport
from src.pedestrian_types.children import Children as children_distribution # @UnresolvedImport
from src.pedestrian_types.elderly import Elderly as elderly_distribution # @UnresolvedImport
from src.pedestrian_types.average import Average as average_distribution # @UnresolvedImport

class Replication:

    def __init__(self, simulationId):       
        try:
            self.simulationId = simulationId
            simulation_log_file = open( "%s.log" % os.path.join(constants.log_dir, simulationId))
            json_str = simulation_log_file.read()
            self.population_log =  json.loads(json_str, cls =PopulationLog_Decoder) 
            self._init_parameters()                 
                   
            self._generate_population_by_log()
        except BaseException as e:
            print( str(e))
            return
    
    def _init_parameters(self):
        self.parameters = self.population_log._get_average_parameter_distributions()._get_parameters()  
           
    def _generate_population_by_log(self):
        self.different_generated_pedestrians = []
        self.average_generated_pedestrians = []
        
        self.different_generated_pedestrian_index = 0
        self.average_generated_pedestrian_index = 0
        
        max_radius = max(self.population_log._get_average_radii_distribution())
        grid_cell_size = max_radius*2+0.05 #multiple 2 because there needs diameter    

        if self.population_log._get_children_num()>0:
            young_pedestrians = self._create_pedestrian_by_log(0, 
                                                            self.population_log._get_children_cell_information(), 
                                                            self.population_log._get_children_radii_distribution(),
                                                            grid_cell_size,
                                                            self.population_log._get_children_seed())    
            
            self.different_generated_pedestrians.extend(young_pedestrians)
            
        if self.population_log._get_elderly_num()>0:
            elderly_pedestrians = self._create_pedestrian_by_log(2, 
                                                            self.population_log._get_elderly_cell_information(), 
                                                            self.population_log._get_elderly_radii_distribubtion(),
                                                            grid_cell_size,
                                                            self.population_log._get_elderly_seed())    
            self.different_generated_pedestrians.extend(elderly_pedestrians)    
        
        
        self.average_generated_pedestrians =  self._create_pedestrian_by_log(3, 
                                                            self.population_log._get_average_cell_information(), 
                                                            self.population_log._get_average_radii_distribution(),
                                                            grid_cell_size,
                                                            self.population_log._get_average_seed())

                     
    def _create_pedestrian_by_log(self, pes_type, designated_cells, radiis, grid_cell_size, seed_value):

        pedestrians_in_same_type =[]
        velocities =[]
        interaction_strengths = []
                 
        if pes_type == 0: # young people
            children_dist = self.population_log._get_children_parameter_distributions()
       
            velocities = children_dist._get_children_desired_velocities_distribution()
            interaction_strengths = children_dist._get_children_interaction_strengths_distribution()
                            
        elif pes_type == 2: # elderly people = 2
            elderly_dist = self.population_log._get_elderly_parameter_distributions()
            
            velocities = elderly_dist._get_elderly_desired_velocities_distribution()
            interaction_strengths =  elderly_dist._get_elderly_interaction_strengths_distribution()
                  
        elif pes_type ==3: # average people =3
            average_dist = self.population_log._get_average_parameter_distributions()
             
            velocities = average_dist._get_average_desired_velocities_distribution()
            interaction_strengths =  average_dist._get_average_interaction_strengths_distribution()
        
        random.seed(seed_value)
        
        for i in range(len(designated_cells)):
            radius = radiis[i]
            velocity = velocities[i]
            cell = designated_cells[i]
            free_space_x = grid_cell_size - radius*2
            x_coord = random.random() * free_space_x + cell[0] + radius
            position = x_coord
            target = cell[1]
            
            pedestrian_id = 0
            if pes_type!=3:
                self.different_generated_pedestrian_index+=1
                pedestrian_id = self.different_generated_pedestrian_index
            else:
                self.average_generated_pedestrian_index +=1
                pedestrian_id = self.average_generated_pedestrian_index
                    
            pedestrians_in_same_type.append(dict(
                p_type = pes_type,
                pedestrian_id = pedestrian_id,
                
                position = position,
                radius = radiis[i],
                initial_position = position,
                
                acceleration = 0.0,
                initial_desired_velocity = velocity,
                velocity = 0.0,
                time = 0.0,
                target = target,
                force_unit = interaction_strengths[i],
                
                desired_force_tracking = 0.0,
                interaction_force_tracking = 0.0))
                   
        return pedestrians_in_same_type    
     
    def _replay(self, prototype=0):
        
        self.timestep = constants.timestep
        self.parameters['timestep'] = self.timestep
        
        self.simulation_duration = constants.total_monitoring_duration_bi_direction
        
        self._init_observation_plots()
     
        #initialize social force model
        force_model.set_parameters(self.parameters)
        
        print("Replay Simulation Id=%s" % self.simulationId )
        
        if prototype ==0 or prototype ==1:
            print(">>> Prototype=%d - Ped_num=%d- scenario=%s " %(1, len(self.different_generated_pedestrians),self.parameters['name']))  
            self._run(self.simulationId, 1, self.different_generated_pedestrians)

        """  reset social force model """         
        force_model.reset_model()
        
        if prototype == 0 or prototype ==2:
            print(">>> Prototype=%d - Ped_num=%d- scenario=%s " %(2, len(self.average_generated_pedestrians),self.parameters['name']))  
            self._run(self.simulationId, 2, self.average_generated_pedestrians)
        
        """ plot observations """ 
        self.plots._save(self.observation_plot_prefix,"rep-%s" % self.simulationId)
          
        """  reset social force model """         
        force_model.reset_model()
                               
    def _init_observation_plots(self):
        self.sample_frequency = int(constants.plot_sample_frequency/self.timestep)
        self.plots = observer_plot(self.parameters,1) #1: replay mode
        self.observation_plot_prefix = os.path.join(constants.observation_dir, self.parameters['name'])
          
    def _init_drawing(self):
        self.show_canvas = image_canvas(
                    self.parameters['drawing_width'],
                    self.parameters['drawing_height'],
                    self.parameters['pixel_factor'],
                    os.path.join(constants.image_dir, self.parameters['name']),
                    os.path.join(constants.video_dir, self.parameters['name']),
                    self.simulationId)
         
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
    
    def _plot_sample(self, prototype,simulation_finished=False):
        escaped_number = int(force_model.get_escaped_num())  
        self.plots._add_sample(prototype, int(self.time), escaped_number)
    
    def _run(self, simulation_id, prototype, pedestrian_population):
      
        self.time = 0.0
        self.frames = 0
        
        if pedestrian_population is not None and len(pedestrian_population)>0:
            for pedestrian in  pedestrian_population:
                force_model.add_pedestrian(pedestrian)
                
        self._init_drawing()  
        finished = False
       
        try:
            while self._tick() and not finished:
                force_model.update_pedestrians()
                
                self._draw()
                
                if not self.frames % self.sample_frequency:
                    self._plot_sample(prototype)
          
                self.time += self.timestep
                self.frames += 1

                if self._done():
                    self._plot_sample(prototype,True)
                    print(">>>>> finished at time= %.3f, frame_num= %d" % (self.time,self.frames))
                    finished = True
                
        except KeyboardInterrupt:
            pass

        self._uninit_drawing()
        