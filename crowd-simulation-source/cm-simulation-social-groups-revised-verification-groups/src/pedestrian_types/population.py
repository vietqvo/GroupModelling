'''
Created on 13 Feb 2015

@author: quangv
'''

from src.pedestrian_types.member import Member as member

class PopulationGenerator:
    
    def __init__(self, parameters, 
                    in_group_a_strength, in_group_a_range,
                    in_group_r_strength, in_group_r_range,
                    out_group_a_strength, out_group_a_range, 
                    out_group_r_strength, out_group_r_range):
        
        self.parameters = parameters
        
        self.total_group_num = len(self.parameters['group_num'])
            
        self.group_generated_pedestrians = []
        
        for group_index in range(self.total_group_num):
            group_num = self.parameters['group_num'][group_index]
            
            group_dist = member(parameters)
                       
            if group_num >0:
                group_dist._generate_member_distribution(group_num,
                                                        in_group_a_strength, in_group_a_range,
                                                        in_group_r_strength, in_group_r_range,
                                                        out_group_a_strength, out_group_a_range, 
                                                        out_group_r_strength, out_group_r_range)
            
                """ add to groups"""
                self.group_generated_pedestrians.append(group_dist)
    
    def _generate_population(self,     
                             placement_radii_info,
                             placement_position_info):
        
        self.generated_group_pedestrians = []
        self.generated_group_member_index = 0 #pedestrian_Id 
        
        """ generate radii for all population based on total_group_num"""
        for i in range(self.total_group_num):
            radii_for_group = placement_radii_info[i]["radii_group"]
            position_group =placement_position_info[i]["position_group"] 

            group_num = self.parameters['group_num'][i]
            group_dist = self.group_generated_pedestrians[i]
            
            group_id = self.parameters['group_id'][i]
            
            if group_num > 0:
                pedestrians= self._create_pedestrian_by_distribution(group_id, group_dist, position_group, radii_for_group)
                if pedestrians is not None and len(pedestrians)>0:
                    for group_member in  pedestrians:                
                        self.generated_group_pedestrians.append(group_member)

     
    def _create_pedestrian_by_distribution(self, group_id, group_dist, designated_positions, radiis):

        pedestrians_in_same_group =[]
        
        in_group_a_strength = group_dist.get_in_group_a_strength()
        in_group_a_range = group_dist.get_in_group_a_range()
        in_group_r_strength = group_dist.get_in_group_r_strength()
        in_group_r_range = group_dist.get_in_group_r_range()
        
        out_group_a_strength = group_dist.get_out_group_a_strength()
        out_group_a_range =  group_dist.get_out_group_a_range()
        out_group_r_strength = group_dist.get_out_group_r_strength()
        out_group_r_range = group_dist.get_out_group_r_range()
      
        for i in range(len(designated_positions)):
      
            pedestrian_id = 0

            self.generated_group_member_index+=1
            pedestrian_id = self.generated_group_member_index
          
            pedestrians_in_same_group.append(dict(
                pedestrian_id = pedestrian_id,#
                group_id = group_id,#
                radius = radiis[i],#
                
                position = designated_positions[i]['position'],#
                
                in_group_a_strength = in_group_a_strength[i],#
                in_group_a_range = in_group_a_range[i],#
                in_group_r_strength = in_group_r_strength[i],#
                in_group_r_range = in_group_r_range[i],
                
                out_group_a_strength = out_group_a_strength[i],#
                out_group_a_range = out_group_a_range[i],
                out_group_r_strength = out_group_r_strength[i],
                out_group_r_range = out_group_r_range[i]))#
                   
        
        return pedestrians_in_same_group
    
    
    def _get_generated_group_pedestrians_population(self): 
        return self.generated_group_pedestrians