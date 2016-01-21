'''
Created on 23 Apr 2015

@author: quangv
'''
import json
from src.pedestrian_types.children import ChildrenLog_Decoder


class PopulationLog(object):
    
    def __init__(self, 
                 group_num,
                 group_parameter_distributions,
                 group_radii_distribution,
                 group_cell_information):
        
        self.group_num = group_num
        self.group_parameter_distributions = group_parameter_distributions
        self.group_radii_distribution = group_radii_distribution
        self.group_cell_information = group_cell_information
       
 
    def _set_group_num(self,group_num):
        self.group_num = group_num
           
    def _get_group_num(self):
        return  self.group_num
    
    def _set_group_parameter_distributions(self,group_parameter_distributions):
        self.group_parameter_distributions = group_parameter_distributions
    
    def _get_group_parameter_distributions(self):
        return self.group_parameter_distributions    
    
    def _set_group_radii_distribution(self,group_radii_distribution):
        self.group_radii_distribution = group_radii_distribution
    
    def _get_children_group_radii_distribution(self):
        return self.group_radii_distribution
    
    def _set_group_cell_information(self,group_cell_information):    
        self.group_cell_information = group_cell_information
    
    def _get_group_cell_information(self):
        return self.group_cell_information
                
    
class PopulationLog_Encoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, PopulationLog):
            return super(PopulationLog_Encoder, self).default(obj)

        return obj.__dict__

class PopulationLog_Decoder(json.JSONDecoder):
    def decode(self,json_string):
     
        default_obj = super(PopulationLog_Decoder,self).decode(json_string)

        group_num = default_obj['group_num']
      
        """ for group information """
        str_group_dist = default_obj['group_parameter_distributions']
        group_dist = json.loads(str_group_dist, cls =ChildrenLog_Decoder)   
        
        group_radii_distribution = []
        for radius in default_obj['group_radii_distribution']:
            group_radii_distribution.append(radius)
        
        group_cell_information = []
        for cell in default_obj['group_cell_information']:
            group_cell_information.append(dict(position = cell["position"], target = cell["target"]))
      
        populationLog = PopulationLog( group_num,
                                       group_dist,
                                       group_radii_distribution,
                                       group_cell_information)
        return populationLog                    