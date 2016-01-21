'''
Created on 29 Sep 2015

@author: quangv
'''
from src.utility.placement import PlacementGenerator 
from src.utility.radii import RadiiGenerator 
import json

class ContextGenerator(object):
    
    def __init__(self, parameters, placement_num):
        
        self.parameters = parameters
        self.radii_generators = []
        self.placement_generators = []
        self.placement_num = placement_num
  
        i = 0
        while i < placement_num:  
              
            radii_generator = RadiiGenerator(self.parameters,
                                              self.parameters['outgroup_num'],
                                              self.parameters['children_group_num'], 
                                              self.parameters['adult_group_num'], 
                                              self.parameters['elder_group_num'])
        
            radii_generator._generate_radii()
            
            position_generator = PlacementGenerator(self.parameters,
                                              self.parameters['outgroup_num'],
                                              self.parameters['children_group_num'], 
                                              self.parameters['adult_group_num'], 
                                              self.parameters['elder_group_num'])
            
            
            position_generator._generate_placements(self.parameters['start_areas'],
                                                    radii_generator._get_max_radii(),
                                                    radii_generator._get_radii_for_young(),
                                                    radii_generator._get_radii_for_adult(),
                                                    radii_generator._get_radii_for_elderly(),
                                                    radii_generator._get_radii_for_outgroup())
        
            self.radii_generators.append(dict(
                    radii_children = radii_generator._get_radii_for_young(),
                    radii_adults = radii_generator._get_radii_for_adult(),
                    radii_elders = radii_generator._get_radii_for_elderly(),
                    radii_outgroup = radii_generator._get_radii_for_outgroup(),
                    max_radii = radii_generator._get_max_radii()))
            
            self.placement_generators.append(dict(        
                    position_children = position_generator._get_placements_for_young(),
                    position_adults = position_generator._get_placements_for_adult(),
                    position_elders = position_generator._get_placements_for_elderly(),
                    position_outgroup = position_generator._get_placements_for_out_group_peds()))

            i+=1
            
    
    def _get_radii_generators(self):
        return self.radii_generators
    
    def _get_placement_generators(self):
        return self.placement_generators
    
    def _set_radii_generators(self,radii_generators):
        self.radii_generators = radii_generators
        
    def _set_placement_generators(self, placement_generators):
        self.placement_generators = placement_generators
           
    def _set_placement_num(self,placement_num):
        self.placement_num = placement_num
        
    def _get_placement_num(self):
        return self.placement_num
   
           
class ContextLog_Encoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, ContextGenerator):
            return super(ContextLog_Encoder, self).default(obj)
        return obj.__dict__

class ContextLog_Decoder(json.JSONDecoder):
    def decode(self,json_string):
     
        default_obj = super(ContextLog_Decoder,self).decode(json_string)
        
        parameters = default_obj['parameters']
        placement_num = default_obj['placement_num']
        
        radii_generators = []
        placement_generators = []
        
        str_radii_generators = default_obj['radii_generators']       
        for radius in str_radii_generators:
            radii_generators.append(dict(radii_children = radius['radii_children'],
                                         radii_adults = radius['radii_adults'],
                                         radii_elders = radius['radii_elders'],
                                         radii_outgroup = radius['radii_outgroup'],
                                         max_radii = radius['max_radii']))
                                       
        
        
        
        str_placement_generators = default_obj['placement_generators']    
        for placement_generator in str_placement_generators:
            placement_generators.append(dict(position_children = placement_generator['position_children'],
                                             position_adults = placement_generator['position_adults'],
                                             position_elders = placement_generator['position_elders'],
                                             position_outgroup = placement_generator['position_outgroup']))

        
        context_generator = ContextGenerator(parameters,placement_num)
        
        context_generator._set_radii_generators(radii_generators)
        context_generator._set_placement_generators(placement_generators)
        
        return context_generator