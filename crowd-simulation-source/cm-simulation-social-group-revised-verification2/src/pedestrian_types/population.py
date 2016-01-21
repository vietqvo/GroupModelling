'''
Created on 13 Feb 2015

@author: quangv
'''

import json

from src.pedestrian_types.children import Children as children_group_distribution
from src.pedestrian_types.population_log import PopulationLog
from src.pedestrian_types.population_log import PopulationLog_Encoder


class PopulationGenerator:
    
    def __init__(self, parameters, 
                 group_num,
                 velocity_mean,
                 relaxation_mean,           
                 interaction_strength_mean,
                 interaction_range_mean,
                 att_strength_mean,
                 att_range_mean):
        
        self.parameters = parameters

        self.group_generated_pedestrians = []

        self.group_dist = children_group_distribution(parameters)

        if group_num >0:
            self.group_dist._generate_children_distribution(group_num,
                                                            velocity_mean, 
                                                           relaxation_mean, 
                                                           interaction_strength_mean,
                                                           interaction_range_mean,
                                                           att_strength_mean,
                                                           att_range_mean)

        
        
        self.total_population_num = group_num
    
    def _generate_population(self,     
                             placement_radii_info,
                             placement_position_info):
  
        """ generate radii for all population """
        
        self.radii_for_group = placement_radii_info["radii_group"]
        self.position_group =placement_position_info["position_group"] 
        
        self.generated_group_pedestrians = []
         
        """ check pedestrian_Id """
        self.generated_group_member_index = 0
        
        if self.total_population_num > 0:
            pedestrians= self._create_pedestrian_by_distribution(0, self.position_group, self.radii_for_group)
            self.generated_group_pedestrians.extend(pedestrians)

     
    def _create_pedestrian_by_distribution(self, pes_type, designated_positions, radiis):

        pedestrians_in_same_type =[]
        velocities =[]
        relaxation_times =[]
        interaction_strengths = []
        interaction_ranges = []
        attraction_strengths = []
        attraction_ranges = []          
        
        if pes_type == 0:
            velocities = self.group_dist._get_children_desired_velocities_distribution()
            relaxation_times = self.group_dist._get_children_relaxation_times_distribution()
            interaction_strengths =  self.group_dist._get_children_interaction_strengths_distribution()
            interaction_ranges = self.group_dist._get_children_interaction_ranges_distribution()
            attraction_strengths = self.group_dist._get_children_att_strengths_distribution()
            attraction_ranges = self.group_dist._get_children_att_ranges_distribution()
    
        for i in range(len(designated_positions)):
      
            pedestrian_id = 0

            self.generated_group_member_index+=1
            pedestrian_id = self.generated_group_member_index
          
            pedestrians_in_same_type.append(dict(
                p_type = pes_type,
                pedestrian_id = pedestrian_id,
                
                position = designated_positions[i]['position'],
                radius = radiis[i],
                initial_position = designated_positions[i]['position'],
                
                acceleration = (0.0, 0.0),
                velocity = (0.0, 0.0),
                time = 0.0,
                
                initial_desired_velocity = velocities[i],
                relax_time = relaxation_times[i],
                max_velocity = velocities[i] * self.parameters['max_velocity_factor'],
                target = designated_positions[i]['target'],
                
                force_unit = interaction_strengths[i],
                interaction_range = interaction_ranges[i],
                
                attraction_strength = attraction_strengths[i],
                attraction_range = attraction_ranges[i]))
                   
        
        return pedestrians_in_same_type
    
    
    def _get_generated_group_pedestrians_population(self): 
        return self.generated_group_pedestrians
    
    def _log_generation(self, log_dir):
        population_log =   PopulationLog(self.total_population_num,
                                         self.group_dist._to_JSON(),
                                         self.radii_for_group,
                                         self.position_group)
        
        log_file = open( "%s.log" % log_dir, "w")

        json_obj = json.dumps(population_log, cls=PopulationLog_Encoder)
        log_file.write(json_obj)
        log_file.close()