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
from src.simulation_observations.pedestrian_track import Pedestrian_Track # @UnresolvedImport
from src.pygame_drawing.drawing import Canvas as image_canvas # @UnresolvedImport
from src.pedestrian_types.population_log import PopulationLog as population_log # @UnresolvedImport
from src.pedestrian_types.population_log import PopulationLog_Decoder # @UnresolvedImport
from src.pedestrian_types.adults import Adults as adults_distribution # @UnresolvedImport
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
        self.parameters = self.population_log._get_average_parameter_distributions().get_parameters()  
        walls = []
        for wall in self.parameters['walls']:         
            walls.append((wall[0],wall[1],wall[2],wall[3]))
        self.parameters['walls'] =  walls
        
        tracking_areas = []
        if self.parameters.get('force_tracking_areas') != None:
            for tracking_area in self.parameters['force_tracking_areas']:         
                tracking_areas.append((tracking_area[0],tracking_area[1],tracking_area[2],tracking_area[3]))
    
        else:#we apply default interaction force measurement in designated area
            
            tracking_areas.append((-5.0,4.0,-2.0,-4.0))
        self.parameters['force_tracking_areas'] =  tracking_areas
           
    def _generate_population_by_log(self):
        self.different_generated_pedestrians = []
        self.average_generated_pedestrians = []
        self.average_cutoff_lv3_generated_pedestrians = []
        self.average_cutoff_lv1_generated_pedestrians = []
        self.uniform_cutoff_lv3_generated_pedestrians = []
        self.uniform_cutoff_lv1_generated_pedestrians = []
        
        
        self.different_generated_pedestrian_index = 0
        self.average_generated_pedestrian_index = 0
        self.average_generated_cutoff_lv3_index = 0
        self.average_generated_cutoff_lv1_index = 0  
        self.uniform_generated_cutoff_lv3_index = 0
        self.uniform_generated_cutoff_lv1_index = 0
        
        
        
        max_radius = max(self.population_log._get_average_radii_distribution())
        grid_cell_size = max_radius*2+0.05 #multiple 2 because there needs diameter    


        """ generate for differential prototype"""
        if self.population_log._get_children_num()>0:
            young_pedestrians = self._create_pedestrian_by_log(0, 
                                                            self.population_log._get_children_cell_information(), 
                                                            self.population_log._get_children_radii_distribution(),
                                                            grid_cell_size,
                                                            self.population_log._get_children_seed())    
            
            self.different_generated_pedestrians.extend(young_pedestrians)
            
        if self.population_log._get_adult_num()>0:
            adult_pedestrians = self._create_pedestrian_by_log(1, 
                                                            self.population_log._get_adult_cell_information(), 
                                                            self.population_log._get_adult_radii_distribution(),
                                                            grid_cell_size,
                                                            self.population_log._get_adult_seed())    
            self.different_generated_pedestrians.extend(adult_pedestrians)
        
        if self.population_log._get_elderly_num()>0:
            elderly_pedestrians = self._create_pedestrian_by_log(2, 
                                                            self.population_log._get_elderly_cell_information(), 
                                                            self.population_log._get_elderly_radii_distribubtion(),
                                                            grid_cell_size,
                                                            self.population_log._get_elderly_seed())    
            self.different_generated_pedestrians.extend(elderly_pedestrians)    
        
        
        """ generate for average prototype"""
        self.average_generated_pedestrians =  self._create_pedestrian_by_log(3, 
                                                            self.population_log._get_average_cell_information(), 
                                                            self.population_log._get_average_radii_distribution(),
                                                            grid_cell_size,
                                                            self.population_log._get_average_seed())

        """ generate average population cutoff_lv3"""
        self.average_cutoff_lv3_generated_pedestrians =  self._create_pedestrian_by_log(4, 
                                                            self.population_log._get_average_cutoff_lv3_cells_distribution(), 
                                                            self.population_log._get_average_cutoff_lv3_radii_distribution(),
                                                            grid_cell_size,
                                                            self.population_log._get_average_cutoff_lv3_seed())
        
        
        """ generate average population cutoff_lv1"""
        self.average_cutoff_lv1_generated_pedestrians =  self._create_pedestrian_by_log(5, 
                                                            self.population_log._get_average_cutoff_lv1_cells_distribution(), 
                                                            self.population_log._get_average_cutoff_lv1_radii_distribution(),
                                                            grid_cell_size,
                                                            self.population_log._get_average_cutoff_lv1_seed())
        
        """ generate uniform population cutoff_lv3"""
        self.uniform_cutoff_lv3_generated_pedestrians =  self._create_pedestrian_by_log(6, 
                                                            self.population_log._get_uniform_cutoff_lv3_cells_distribution(), 
                                                            self.population_log._get_uniform_cutoff_lv3_radii_distribution(),
                                                            grid_cell_size,
                                                            self.population_log._get_uniform_cutoff_lv3_seed())
        
        """ generate uniform population cutoff_lv1"""
        self.uniform_cutoff_lv1_generated_pedestrians =  self._create_pedestrian_by_log(7, 
                                                            self.population_log._get_uniform_cutoff_lv1_cells_distribution(), 
                                                            self.population_log._get_uniform_cutoff_lv1_radii_distribution(),
                                                            grid_cell_size,
                                                            self.population_log._get_uniform_cutoff_lv1_seed())
                     
    def _create_pedestrian_by_log(self, pes_type, designated_cells, radiis, grid_cell_size, seed_value):

        pedestrians_in_same_type =[]
        velocities =[]
        relaxation_times =[]
        interaction_strengths = []
        interaction_ranges = []
                 
        if pes_type == 0: # young people
            children_dist = self.population_log._get_children_parameter_distributions()
       
            velocities = children_dist._get_children_desired_velocities_distribution()
            relaxation_times = children_dist._get_children_relaxation_times_distribution()
            interaction_strengths = children_dist._get_children_interaction_strengths_distribution()
            interaction_ranges = children_dist._get_children_interaction_ranges_distribution()
          

        elif pes_type ==1: # adult people
            adults_dist = self.population_log._get_adult_parameter_distributions()
            
            velocities = adults_dist._get_adults_desired_velocities_distribution()
            relaxation_times = adults_dist._get_adults_relaxation_times_distribution()
            interaction_strengths =  adults_dist._get_adults_interaction_strengths_distribution()
            interaction_ranges = adults_dist._get_adults_interaction_ranges_distribution() 
        
                     
        elif pes_type == 2: # elderly people = 2
            elderly_dist = self.population_log._get_elderly_parameter_distributions()
            
            velocities = elderly_dist._get_elderly_desired_velocities_distribution()
            relaxation_times = elderly_dist._get_elderly_relaxation_times_distribution()
            interaction_strengths =  elderly_dist._get_elderly_interaction_strengths_distribution()
            interaction_ranges = elderly_dist._get_elderly_interaction_ranges_distribution()
          
                 
        elif pes_type ==3: # average people =3
            average_dist = self.population_log._get_average_parameter_distributions()
             
            velocities = average_dist.get_average_desired_velocities()
            relaxation_times = average_dist.get_average_relaxation_times()
            interaction_strengths =  average_dist.get_average_interaction_strengths()
            interaction_ranges = average_dist.get_average_interaction_ranges()
        
        elif pes_type ==4: #average cutoff level 3
            average_dist = self.population_log._get_average_parameter_distributions()
             
            velocities = average_dist.get_average_cutoff_lv_3_desired_velocities()
            relaxation_times = average_dist.get_average_cutoff_lv_3_relaxation_times()
            interaction_strengths =  average_dist.get_average_cutoff_lv_3_interaction_strengths()
            interaction_ranges = average_dist.get_average_cutoff_lv_3_interaction_ranges()
        
        elif pes_type ==5: #average cutoff level 1
            average_dist = self.population_log._get_average_parameter_distributions()
             
            velocities = average_dist.get_average_cutoff_lv_1_desired_velocities()
            relaxation_times = average_dist.get_average_cutoff_lv_1_relaxation_times()
            interaction_strengths =  average_dist.get_average_cutoff_lv_1_interaction_strengths()
            interaction_ranges = average_dist.get_average_cutoff_lv_1_interaction_ranges()
        
        elif pes_type ==6: #uniform cutoff level 3
            average_dist = self.population_log._get_average_parameter_distributions()
             
            velocities = average_dist.get_uniform_cutoff_lv_3_desired_velocities()
            relaxation_times = average_dist.get_uniform_cutoff_lv_3_relaxation_times()
            interaction_strengths =  average_dist.get_uniform_cutoff_lv_3_interaction_strengths()
            interaction_ranges = average_dist.get_uniform_cutoff_lv_3_interaction_ranges()
        
        elif pes_type ==7: #uniform cutoff level 1
            average_dist = self.population_log._get_average_parameter_distributions()
             
            velocities = average_dist.get_uniform_cutoff_lv_1_desired_velocities()
            relaxation_times = average_dist.get_uniform_cutoff_lv_1_relaxation_times()
            interaction_strengths =  average_dist.get_uniform_cutoff_lv_1_interaction_strengths()
            interaction_ranges = average_dist.get_uniform_cutoff_lv_1_interaction_ranges()
        
        random.seed(seed_value)
        
        for i in range(len(designated_cells)):
            radius = radiis[i]
            velocity = velocities[i]
            cell = designated_cells[i]
            free_space_x = grid_cell_size - radius*2
            free_space_y = grid_cell_size - radius*2
            x_coord = random.random() * free_space_x + cell[0] + radius
            y_coord = random.random() * free_space_y + cell[1] + radius
            position = (x_coord, y_coord)
            target_x = cell[2][0]
            target_y= cell[2][1]
            target =(target_x,target_y)
            
            pedestrian_id = 0
            if pes_type ==0 or pes_type == 1 or pes_type == 2:
                self.different_generated_pedestrian_index+=1
                pedestrian_id = self.different_generated_pedestrian_index
            
            elif pes_type == 3:
                self.average_generated_pedestrian_index +=1
                pedestrian_id = self.average_generated_pedestrian_index
                               
            elif pes_type == 4:
                self.average_generated_cutoff_lv3_index +=1
                pedestrian_id = self.average_generated_cutoff_lv3_index
                
            elif pes_type == 5:
                self.average_generated_cutoff_lv1_index +=1
                pedestrian_id = self.average_generated_cutoff_lv1_index    
            
            elif pes_type == 6:
                self.uniform_generated_cutoff_lv3_index +=1
                pedestrian_id = self.uniform_generated_cutoff_lv3_index
            
            elif pes_type == 7:
                self.uniform_generated_cutoff_lv1_index +=1
                pedestrian_id = self.uniform_generated_cutoff_lv1_index    
                
            pedestrians_in_same_type.append(dict(
                p_type = pes_type,
                pedestrian_id = pedestrian_id,
                 
                position = position,
                radius = radiis[i],
                initial_position = position,
                
                acceleration = (0.0, 0.0),
                initial_desired_velocity = velocity,
                velocity = (0.0, 0.0),
                time = 0.0,
                relax_time = relaxation_times[i],
                max_velocity = velocity * self.parameters['max_velocity_factor'],
                target = target,
                 
                force_unit = interaction_strengths[i],
                interaction_range = interaction_ranges[i],
                interaction_lamda = self.parameters['lambda'],
                
                desired_force_tracking = (0.0,0.0),
                interaction_force_tracking = (0.0,0.0),
                obstacle_force_tracking = (0.0,0.0)))
        
        return pedestrians_in_same_type    
     
    def _replay(self, prototype=0):
        
        self.timestep = constants.timestep
        self.parameters['timestep'] = self.timestep
        
        if len(self.parameters['start_areas']) ==1:
            self.simulation_duration = constants.total_monitoring_duration_uni_direction
        else:
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
        
        if prototype == 0 or prototype ==2: # run for average prototype
            print(">>> Prototype=%d - Ped_num=%d- scenario=%s " %(2, len(self.average_generated_pedestrians),self.parameters['name']))  
            self._run(self.simulationId, 2, self.average_generated_pedestrians)
        
        
        """  reset social force model """         
        force_model.reset_model()
               
        if prototype == 0 or prototype ==3: # run for average cutoff level 3 prototype
            print(">>> Prototype=%d - Ped_num=%d- scenario=%s " %(3, len(self.average_cutoff_lv3_generated_pedestrians),self.parameters['name']))  
            self._run(self.simulationId, 3, self.average_cutoff_lv3_generated_pedestrians)
        
        """  reset social force model """         
        force_model.reset_model()
               
        if prototype == 0 or prototype ==4: # run for average cutoff level 1 prototype
            print(">>> Prototype=%d - Ped_num=%d- scenario=%s " %(4, len(self.average_cutoff_lv1_generated_pedestrians),self.parameters['name']))  
            self._run(self.simulationId, 4, self.average_cutoff_lv1_generated_pedestrians)
      
        """  reset social force model """         
        force_model.reset_model()
               
        if prototype == 0 or prototype ==5: # run for uniform cutoff level 3 prototype
            print(">>> Prototype=%d - Ped_num=%d- scenario=%s " %(5, len(self.uniform_cutoff_lv3_generated_pedestrians),self.parameters['name']))  
            self._run(self.simulationId, 5, self.uniform_cutoff_lv3_generated_pedestrians)
            
        """  reset social force model """         
        force_model.reset_model()
               
        if prototype == 0 or prototype ==6: # run for uniform cutoff level 1 prototype
            print(">>> Prototype=%d - Ped_num=%d- scenario=%s " %(6, len(self.uniform_cutoff_lv1_generated_pedestrians),self.parameters['name']))  
            self._run(self.simulationId, 6, self.uniform_cutoff_lv1_generated_pedestrians)
       
           
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
        
        self.tracked_current_velocity = 0.0
        self.tracked_panic_level = 0.0
        self.tracked_desired_velocity = 0.0
        self.tracked_desire_force = 0.0
        self.tracked_interaction_force = 0.0
        self.tracked_obstacle_force = 0.0
        
        self.tracked_desired_force_vector = (0.0,0.0)
        self.tracked_interaction_force_vector = (0.0,0.0)
        self.tracked_obstacle_force_vector = (0.0,0.0)
        self.tracked_initial_position = (0.0,0.0)
        
        population_number = int(force_model.get_population_size())
        for i in range(population_number):
            (x,y) = force_model.a_property(i, "position")
            if math.isnan(x) ==False and math.isnan(y)==False:
                r = force_model.a_property(i, "radius")
                t = force_model.a_property(i, "p_type")
                
                if self.tracked_pedestrian_id == -1:
                    is_tracked = self._canvas("is_tracked_pedestrian", x,y)           
                    if is_tracked:
                        self.tracked_pedestrian_id = force_model.a_property(i, "id")
                        #initialize pedestrian track
                        print("Tracked pedestrian Id %s"% str(self.tracked_pedestrian_id))
                        initial_v = force_model.a_property(i, "initial_velocity")
                        max_v = force_model.a_property(i, "max_velocity")
                        relax_time = force_model.a_property(i, "relax_time")
                        self.pedestrian_track = Pedestrian_Track(self.tracked_pedestrian_id, initial_v,max_v,relax_time)
                        
                        self.tracked_current_velocity = force_model.a_property(i, "velocity")
                        self.tracked_panic_level = force_model.a_property(i, "impatience_level")
                        self.tracked_desired_velocity = force_model.a_property(i,"desired_velocity")
                        self.tracked_desire_force = force_model.a_property(i, "desired_force")
                        
                        self.tracked_interaction_force = force_model.a_property(i, "interaction_force")
                        self.tracked_obstacle_force = force_model.a_property(i, "obstacle_force")
                        
                        
                        self.tracked_desired_force_vector = force_model.a_property(i, "desired_force_v")
                        self.tracked_interaction_force_vector = force_model.a_property(i, "interaction_force_v")
                        self.tracked_obstacle_force_vector = force_model.a_property(i, "obstacle_force_v")
                        
                        self.tracked_initial_position = force_model.a_property(i, "initial_position")
                        self._canvas("draw_pedestrian", x,y,r,t,1,
                                     self.tracked_desired_force_vector,
                                     self.tracked_interaction_force_vector,
                                     self.tracked_obstacle_force_vector,
                                     self.tracked_initial_position)
                        
                    else:
                        self._canvas("draw_pedestrian", x,y,r,t) 
                else:
                    if  self.tracked_pedestrian_id == force_model.a_property(i, "id"):
                        
                        self.tracked_current_velocity = force_model.a_property(i, "velocity")
                        self.tracked_panic_level = force_model.a_property(i, "impatience_level")
                        self.tracked_desired_velocity = force_model.a_property(i,"desired_velocity")
                        self.tracked_desire_force = force_model.a_property(i, "desired_force")
                        
                        self.tracked_interaction_force = force_model.a_property(i, "interaction_force")
                        self.tracked_obstacle_force = force_model.a_property(i, "obstacle_force")
                        
                        self.tracked_desired_force_vector = force_model.a_property(i, "desired_force_v")
                        self.tracked_interaction_force_vector = force_model.a_property(i, "interaction_force_v")
                        self.tracked_obstacle_force_vector = force_model.a_property(i, "obstacle_force_v")
                        self.tracked_initial_position = force_model.a_property(i, "initial_position")
                                                
                        self._canvas("draw_pedestrian", x,y,r,t,1,
                                     self.tracked_desired_force_vector,
                                     self.tracked_interaction_force_vector,
                                     self.tracked_obstacle_force_vector,
                                     self.tracked_initial_position)
                    else:
                        self._canvas("draw_pedestrian", x,y,r,t)    
            else:
                print("Position is unidentified")
                sys.exit()
        
        #reset tracked position of screen
        if self.tracked_pedestrian_id == -1:
            self._canvas("reset_tracked_position")         
                  
                 
        self._canvas("draw_text", "t = %.2f" % self.time)
        
        for t in self.parameters['targets']:
            self._canvas("draw_target", *t)
       
        for w in self.parameters['walls']:
            self._canvas("draw_wall", w)
       
        for s in self.parameters['start_areas']:
            self._canvas("draw_start_area", s)
        
        for m in self.parameters['force_tracking_areas']:
            self._canvas("draw_force_tracking_area",m)
                
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
        panic_level = force_model.get_total_panic_level()
        interaction_force = force_model.get_total_interaction_force()
        if math.isnan(panic_level):
            panic_level = 0
            
        self.plots._add_sample(prototype, int(self.time), escaped_number,panic_level,interaction_force)
         
        """ plot tracking pedestrian p when he hasn't yet escaped"""
        if  self.tracked_pedestrian_id !=-1:  
            checked_pedestrian_escaped = force_model.check_escaped(self.tracked_pedestrian_id)
            if  checked_pedestrian_escaped==1 or simulation_finished==True:
                prefix = os.path.join(constants.pedestrian_track_dir, self.parameters['name'])
                self.pedestrian_track._save(prefix, self.simulationId)          
   
                self.tracked_pedestrian_id =-1
                self._canvas("reset_tracked_position")         
            else:
                self.pedestrian_track._add_sample(int(self.time),
                                                  self.tracked_current_velocity,
                                                  self.tracked_panic_level,
                                                  self.tracked_desired_velocity,
                                                  
                                                  self.tracked_desire_force,
                                                  self.tracked_interaction_force,
                                                  self.tracked_obstacle_force)
            
    def _run(self, simulation_id, prototype, pedestrian_population):
      
        self.time = 0.0
        self.frames = 0
        
        if pedestrian_population is not None and len(pedestrian_population)>0:
            for pedestrian in  pedestrian_population:
                force_model.add_pedestrian(pedestrian)
                
        self._init_drawing()
        
        self.tracked_pedestrian_id = -1  
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
        