'''
Created on 23 Apr 2015

@author: quangv
'''
import json
from src.pedestrian_types.children import ChildrenLog_Decoder
from src.pedestrian_types.adults import AdultLog_Decoder
from src.pedestrian_types.elderly import ElderlyLog_Decoder
from src.pedestrian_types.outgroup_peds import OutGroup_Peds_Log_Decoder

class PopulationLog(object):
    
    def __init__(self, 
                 children_group_num,
                 adults_group_num,
                 elderly_group_num,
                 outgroup_num,
                 
                 children_group_parameter_distributions,
                 children_group_radii_distribution,
                 children_group_cell_information,                
                  
                 adult_group_parameter_distributions,
                 adult_group_radii_distribution,
                 adult_group_cell_information,
                 
                 elderly_group_parameter_distributions,
                 elderly_group_radii_distribution,
                 elderly_group_cell_information,
                 
                 outgroup_parameter_distributions,
                 outgroup_radii_distribution,
                 outgroup_cell_information):
        
        self.children_group_num = children_group_num
        self.adults_group_num = adults_group_num
        self.elderly_group_num = elderly_group_num
        self.outgroup_num = outgroup_num
        
        self.children_group_parameter_distributions = children_group_parameter_distributions
        self.children_group_radii_distribution = children_group_radii_distribution
        self.children_group_cell_information = children_group_cell_information
       
        self.adult_group_parameter_distributions = adult_group_parameter_distributions
        self.adult_group_radii_distribution = adult_group_radii_distribution
        self.adult_group_cell_information = adult_group_cell_information
        
        self.elderly_group_parameter_distributions = elderly_group_parameter_distributions
        self.elderly_group_radii_distribution = elderly_group_radii_distribution
        self.elderly_group_cell_information = elderly_group_cell_information
        
        self.outgroup_parameter_distributions = outgroup_parameter_distributions
        self.outgroup_radii_distribution = outgroup_radii_distribution
        self.outgroup_cell_information = outgroup_cell_information
        
    def _set_children_group_num(self,children_group_num):
        self.children_group_num = children_group_num
    
    def _set_adults_group_num(self,adults_group_num):
        self.adults_group_num = adults_group_num
    
    def _set_elderly_group_num(self,elderly_group_num):
        self.elderly_group_num = elderly_group_num
    
    def _set_outgroup_num(self,outgroup_num):
        self.outgroup_num = outgroup_num
        
        
    def _get_children_group_num(self):
        return  self.children_group_num
    
    def _get_adults_group_num(self):
        return  self.adults_group_num
    
    def _get_elderly_group_num(self):
        return  self.elderly_group_num

    def _get_outgroup_num(self):
        return self.outgroup_num
    
    def _set_children_group_parameter_distributions(self,children_group_parameter_distributions):
        self.children_group_parameter_distributions = children_group_parameter_distributions
    
    def _get_children_group_parameter_distributions(self):
        return self.children_group_parameter_distributions    
    
    def _set_children_group_radii_distribution(self,children_group_radii_distribution):
        self.children_group_radii_distribution = children_group_radii_distribution
    
    def _get_children_group_radii_distribution(self):
        return self.children_group_radii_distribution
    
    def _set_children_group_cell_information(self,children_group_cell_information):    
        self.children_group_cell_information = children_group_cell_information
    
    def _get_children_group_cell_information(self):
        return self.children_group_cell_information
                
    def _set_adult_group_parameter_distributions(self,adult_group_parameter_distributions):
        self.adult_group_parameter_distributions = adult_group_parameter_distributions
    
    def _get_adult_group_parameter_distributions(self):
        return self.adult_group_parameter_distributions    
    
    def _set_adult_group_radii_distribution(self,adult_group_radii_distribution):
        self.adult_group_radii_distribution = adult_group_radii_distribution
    
    def _get_adult_group_radii_distribution(self):
        return self.adult_group_radii_distribution
    
    def _set_adult_group_cell_information(self,adult_group_cell_information):    
        self.adult_group_cell_information = adult_group_cell_information
    
    def _get_adult_group_cell_information(self):
        return self.adult_group_cell_information
            
    def _set_elderly_group_parameter_distributions(self,elderly_group_parameter_distributions):
        self.elderly_group_parameter_distributions = elderly_group_parameter_distributions
    
    def _get_elderly_group_parameter_distributions(self):
        return self.elderly_group_parameter_distributions    
    
    def _set_elderly_group_radii_distribution(self,elderly_group_radii_distribution):
        self.elderly_group_radii_distribution = elderly_group_radii_distribution
    
    def _get_elderly_group_radii_distribution(self):
        return self.elderly_group_radii_distribution
    
    def _set_elderly_group_cell_information(self,elderly_group_cell_information):    
        self.elderly_group_cell_information = elderly_group_cell_information
    
    def _get_elderly_group_cell_information(self):
        return self.elderly_group_cell_information
    
    def _set_outgroup_parameter_distributions(self,outgroup_parameter_distributions):
        self.outgroup_parameter_distributions = outgroup_parameter_distributions
    
    def _get_outgroup_parameter_distributions(self):
        return self.outgroup_parameter_distributions    
    
    def _set_outgroup_radii_distribution(self,outgroup_radii_distribution):
        self.outgroup_radii_distribution = outgroup_radii_distribution
    
    def _get_outgroup_radii_distribution(self):
        return self.outgroup_radii_distribution
    
    def _set_outgroup_cell_information(self,outgroup_cell_information):    
        self.outgroup_cell_information = outgroup_cell_information
    
    def _get_outgroup_cell_information(self):
        return self.outgroup_cell_information
    
class PopulationLog_Encoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, PopulationLog):
            return super(PopulationLog_Encoder, self).default(obj)

        return obj.__dict__

class PopulationLog_Decoder(json.JSONDecoder):
    def decode(self,json_string):
     
        default_obj = super(PopulationLog_Decoder,self).decode(json_string)

        children_group_num = default_obj['children_group_num']
        adults_group_num = default_obj['adults_group_num']
        elderly_group_num = default_obj['elderly_group_num']
        outgroup_num = default_obj['outgroup_num']
        
        """ for children information """
        str_children_dist = default_obj['children_group_parameter_distributions']
        childrent_dist = json.loads(str_children_dist, cls =ChildrenLog_Decoder)   

        
        children_group_radii_distribution = []
        for radius in default_obj['children_group_radii_distribution']:
            children_group_radii_distribution.append(radius)
        
        children_group_cell_information = []
        for cell in default_obj['children_group_cell_information']:
            children_group_cell_information.append(dict(position = cell["position"], target = cell["target"]))
                    
        """ for adult information """
        str_adult_dist = default_obj['adult_group_parameter_distributions']
        adult_dist = json.loads(str_adult_dist, cls =AdultLog_Decoder)   
         
        adult_group_radii_distribution = []
        for radius in default_obj['adult_group_radii_distribution']:
            adult_group_radii_distribution.append(radius)
        
 
        adult_group_cell_information = []
        for cell in default_obj['adult_group_cell_information']:
            adult_group_cell_information.append(dict(position = cell["position"], target = cell["target"]))
             
        """ for elderly information """
        str_elderly_dist = default_obj['elderly_group_parameter_distributions']
        elderly_dist = json.loads(str_elderly_dist, cls =ElderlyLog_Decoder)   
      
        elderly_group_radii_distribution = []
        for radius in default_obj['elderly_group_radii_distribution']:
            elderly_group_radii_distribution.append(radius)
        
        elderly_group_cell_information = []
        for cell in default_obj['elderly_group_cell_information']:
            elderly_group_cell_information.append(dict(position = cell["position"], target = cell["target"]))
        
        """ for out group information """
        str_outgroup_dist = default_obj['outgroup_parameter_distributions']
        outgroup_dist = json.loads(str_outgroup_dist, cls =OutGroup_Peds_Log_Decoder)   
      
        outgroup_radii_distribution = []
        for radius in default_obj['outgroup_radii_distribution']:
            outgroup_radii_distribution.append(radius)
            
        outgroup_cell_information = []
        for cell in default_obj['outgroup_cell_information']:
            outgroup_cell_information.append(dict(position = cell["position"], target = cell["target"]))
        
        populationLog = PopulationLog( children_group_num,
                 adults_group_num,
                 elderly_group_num,
                 outgroup_num,
                 
                 childrent_dist,
                 children_group_radii_distribution,
                 children_group_cell_information,                
                                  
                 adult_dist,
                 adult_group_radii_distribution,
                 adult_group_cell_information,
                 
                 elderly_dist,
                 elderly_group_radii_distribution,
                 elderly_group_cell_information,
                 
                 outgroup_dist,
                 outgroup_radii_distribution,
                 outgroup_cell_information)
        return populationLog                    