'''
Created on 23 Apr 2015

@author: quangv
'''
import sys
import os, math
import json
from src import constants # @UnresolvedImport
from src import socialforce as force_model  # @UnresolvedImport
from src.simulation_observations.observations import ObservationPlots as observer_plot # @UnresolvedImport
from src.pygame_drawing.drawing import Canvas as image_canvas # @UnresolvedImport
from src.pedestrian_types.population_log import PopulationLog as population_log # @UnresolvedImport
from src.pedestrian_types.population_log import PopulationLog_Decoder # @UnresolvedImport
from src.pedestrian_types.adults import Adults as adults_distribution # @UnresolvedImport
from src.pedestrian_types.children import Children as children_distribution # @UnresolvedImport
from src.pedestrian_types.elderly import Elderly as elderly_distribution # @UnresolvedImport
from src.pedestrian_types.outgroup_peds import Outgroup_peds as outgroup_peds_distribution # @UnresolvedImport

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
        self.parameters = self.population_log._get_outgroup_parameter_distributions().get_parameters()  
        walls = []
        for wall in self.parameters['walls']:         
            walls.append((wall[0],wall[1],wall[2],wall[3]))
        self.parameters['walls'] =  walls
             
    def _generate_population_by_log(self):
        self.generated_group_pedestrians = []
        self.generated_out_group_pedestrians = []
        
        self.generated_group_member_index = 0
        self.generated_out_group_pedestrian_index = self.population_log._get_children_group_num() + self.population_log._get_adults_group_num() + self.population_log._get_elderly_group_num() -1  ##index order 
        
        """ generate for group members"""
        if self.population_log._get_children_group_num()>0:
            young_group_pedestrians = self._create_pedestrian_by_log(0, 
                                                            self.population_log._get_children_group_cell_information(), 
                                                            self.population_log._get_children_group_radii_distribution())    
            self.generated_group_pedestrians.extend(young_group_pedestrians)
            
        if self.population_log._get_adults_group_num()>0:
            adult_group_pedestrians = self._create_pedestrian_by_log(1, 
                                                            self.population_log._get_adult_group_cell_information(), 
                                                            self.population_log._get_adult_group_radii_distribution())    
            self.generated_group_pedestrians.extend(adult_group_pedestrians)
        
        if self.population_log._get_elderly_group_num()>0:
            elderly_group_pedestrians = self._create_pedestrian_by_log(2, 
                                                            self.population_log._get_elderly_group_cell_information(), 
                                                            self.population_log._get_elderly_group_radii_distribution())    
            self.generated_group_pedestrians.extend(elderly_group_pedestrians)    
        
        
        """ generate for out group member"""
        if self.population_log._get_outgroup_num()>0:
            self.generated_out_group_pedestrians =  self._create_pedestrian_by_log(3, 
                                                            self.population_log._get_outgroup_cell_information(), 
                                                            self.population_log._get_outgroup_radii_distribution())

     
                     
    def _create_pedestrian_by_log(self, pes_type, designated_positions, radiis):

        pedestrians_in_same_type =[]
        velocities =[]
        relaxation_times =[]
        interaction_strengths = []
        interaction_ranges = []
                 
        if pes_type == 0: # young member people
            children_dist = self.population_log._get_children_group_parameter_distributions()
       
            velocities = children_dist._get_children_desired_velocities_distribution()
            relaxation_times = children_dist._get_children_relaxation_times_distribution()
            interaction_strengths = children_dist._get_children_interaction_strengths_distribution()
            interaction_ranges = children_dist._get_children_interaction_ranges_distribution()
          

        elif pes_type ==1: # adult member people
            adults_dist = self.population_log._get_adult_group_parameter_distributions()
            
            velocities = adults_dist._get_adults_desired_velocities_distribution()
            relaxation_times = adults_dist._get_adults_relaxation_times_distribution()
            interaction_strengths =  adults_dist._get_adults_interaction_strengths_distribution()
            interaction_ranges = adults_dist._get_adults_interaction_ranges_distribution() 
        
                     
        elif pes_type == 2: # elderly member people = 2
            elderly_dist = self.population_log._get_elderly_group_parameter_distributions()
            
            velocities = elderly_dist._get_elderly_desired_velocities_distribution()
            relaxation_times = elderly_dist._get_elderly_relaxation_times_distribution()
            interaction_strengths =  elderly_dist._get_elderly_interaction_strengths_distribution()
            interaction_ranges = elderly_dist._get_elderly_interaction_ranges_distribution()
          
                 
        elif pes_type ==3: # out group member people =3
            outgroup_dist = self.population_log._get_outgroup_parameter_distributions()
             
            velocities = outgroup_dist.get_outgroup_desired_velocities()
            relaxation_times = outgroup_dist.get_outgroup_relaxation_times()
            interaction_strengths =  outgroup_dist.get_outgroup_interaction_strengths()
            interaction_ranges = outgroup_dist.get_outgroup_interaction_ranges()
        
        for i in range(len(designated_positions)):
            pedestrian_id = 0
            
            if pes_type ==0 or pes_type == 1 or pes_type == 2:
                self.generated_group_member_index+=1
                pedestrian_id = self.generated_group_member_index
            
            elif pes_type == 3:
                self.generated_out_group_pedestrian_index +=1
                pedestrian_id = self.generated_out_group_pedestrian_index
                        
            pedestrians_in_same_type.append(dict(
                p_type = pes_type,
                pedestrian_id = pedestrian_id,
                 
                position = designated_positions[i]['position'],
                radius = radiis[i],
                initial_position = designated_positions[i]['position'],
                
                acceleration = (0.0, 0.0),
                initial_desired_velocity = velocities[i],
                velocity = (0.0, 0.0),
                time = 0.0,
                relax_time = relaxation_times[i],
                max_velocity = velocities[i] * self.parameters['max_velocity_factor'],
                target = (designated_positions[i]['target'][0],designated_positions[i]['target'][1]),
                 
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

        self._run(self.simulationId, self.generated_group_pedestrians,self.generated_out_group_pedestrians) 
        
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
        
        group_population_number = int(force_model.get_group_size())
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
        self._canvas("draw_group_center", group_center_x,group_center_y)
                
        out_group_population_number = int(force_model.get_out_group_size())
        for i in range(out_group_population_number):
            (x,y) = force_model.out_group_pedestrian_a_property(i, "position")
            if math.isnan(x) ==False and math.isnan(y)==False:
                r = force_model.out_group_pedestrian_a_property(i, "radius")
                t = force_model.out_group_pedestrian_a_property(i, "p_type")
                self._canvas("draw_pedestrian", x,y,r,t)
            else:
                print("Position is unidentified")
                sys.exit()
                        
        self._canvas("draw_text", "t = %.2f" % self.time)
        
        for t in self.parameters['targets']:
            self._canvas("draw_target", *t)
       
        for w in self.parameters['walls']:
            self._canvas("draw_wall", w)
       
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
        group_cohesion_degree = force_model.get_group_cohesion_degree()
        group_average_speed = force_model.get_group_average_speed()
        group_average_direction = force_model.get_group_average_direction()
        
        self.plots._add_sample(int(self.time), group_cohesion_degree, group_average_speed, group_average_direction, escaped_number)
  
            
    def _run(self, simulation_id, group_pedestrians,outgroup_pedestrians): 
      
        self.time = 0.0
        self.frames = 0
        
        if group_pedestrians is not None and len(group_pedestrians)>0:
            for group_member in  group_pedestrians:                
                force_model.add_group_pedestrian(group_member)
        
        if outgroup_pedestrians is not None and len(outgroup_pedestrians)>0:
            for pedestrian in  outgroup_pedestrians:                
                force_model.add_out_group_pedestrian(pedestrian)
                
        self._init_drawing()
        
        finished = False
       
        try:
            while self._tick() and not finished:
                force_model.update_pedestrians()
                
                self._draw()
                
                if not self.frames % self.sample_frequency:
                    self._plot_sample()
          
                self.time += self.timestep
                self.frames += 1

                if self._done():
                    self._plot_sample()
                    print(">>>>> finished at time= %.3f, frame_num= %d" % (self.time,self.frames))
                    finished = True
                
        except KeyboardInterrupt:
            pass

        self._uninit_drawing()
        