'''
Created on 28 Sep 2015

@author: quangv
'''
class PlacementGenerator(object):
    
    def __init__(self, parameters, group_num):
        self.parameters = parameters
     
        self._reset_placements()
        
        self.total_population_num = group_num
             
    def _reset_placements(self):
        
        self.max_radius = 0
        self.placements_for_group = []

    def _generate_placements(self, start_areas):
        
        if self.total_population_num > 0:
            self.placements_for_group= self._create_placement_for_pedestrian_type(0, start_areas) 
              
    def _create_placement_for_pedestrian_type(self,pes_type, start_areas):
        
        pedestrians_in_same_type =[]
    
        for i in range(2):
            position = start_areas[0][i]
            
            pedestrians_in_same_type.append(dict(
                position = position))
                    
        return pedestrians_in_same_type
     
    def _get_max_radius(self):
        return self.max_radius
    
    def _set_max_radius(self,radius):
        self.max_radius = radius
        
    def _get_placements_for_group(self):
        return self.placements_for_group      
    
    def _set_placements_for_group(self,placements):
        self.placements_for_group = placements   
    
    def _get_total_population(self):
        return self.total_population_num
    
    def _set_total_population(self,total_num):
        self.total_population_num = total_num