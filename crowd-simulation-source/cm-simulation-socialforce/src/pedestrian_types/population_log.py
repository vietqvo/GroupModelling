'''
Created on 23 Apr 2015

@author: quangv
'''
import json
from src.pedestrian_types.children import ChildrenLog_Decoder
from src.pedestrian_types.adults import AdultLog_Decoder
from src.pedestrian_types.elderly import ElderlyLog_Decoder
from src.pedestrian_types.average import AverageLog_Decoder

class PopulationLog(object):
    
    def __init__(self, 
                 children_num,
                 adult_num,
                 elderly_num,
                 
                 children_parameter_distributions,
                 children_radii_distribution,
                 children_cell_information,                
                 children_seed,
                 
                 adult_parameter_distributions,
                 adult_radii_distribution,
                 adult_cell_information,
                 adult_seed,
                 
                 elderly_parameter_distributions,
                 elderly_radii_distribubtion,
                 elderly_cell_information,
                 elderly_seed,
                 
                 average_parameter_distributions,
                 average_radii_distribution,
                 average_cell_information,
                 average_seed
                 ):
        self.children_num = children_num
        self.adult_num = adult_num
        self.elderly_num = elderly_num
        
        self.children_parameter_distributions = children_parameter_distributions
        self.children_radii_distribution = children_radii_distribution
        self.children_cell_information = children_cell_information
        self.children_seed = children_seed
        
        self.adult_parameter_distributions = adult_parameter_distributions
        self.adult_radii_distribution = adult_radii_distribution
        self.adult_cell_information = adult_cell_information
        self.adult_seed = adult_seed
        
        self.elderly_parameter_distributions = elderly_parameter_distributions
        self.elderly_radii_distribubtion = elderly_radii_distribubtion
        self.elderly_cell_information = elderly_cell_information
        self.elderly_seed = elderly_seed
        
        self.average_parameter_distributions = average_parameter_distributions
        self.average_radii_distribution = average_radii_distribution
        self.average_cell_information = average_cell_information      
        self.average_seed = average_seed
        
    def _get_children_num(self):
        return self.children_num
    
    def _get_adult_num(self):
        return self.adult_num
    
    def _get_elderly_num(self):
        return self.elderly_num
    
    def _get_children_parameter_distributions(self):
        return self.children_parameter_distributions
    
    def _get_children_radii_distribution(self):
        return self.children_radii_distribution
    
    def _get_children_cell_information(self):
        return self.children_cell_information
    
    def _get_children_seed(self):
        return self.children_seed
    
    def _get_adult_parameter_distributions(self):
        return self.adult_parameter_distributions
    
    def _get_adult_radii_distribution(self):
        return self.adult_radii_distribution
    
    def _get_adult_cell_information(self):
        return self.adult_cell_information
    
    def _get_adult_seed(self):
        return self.adult_seed
    
    def _get_elderly_parameter_distributions(self):
        return self.elderly_parameter_distributions
    
    def _get_elderly_radii_distribubtion(self):
        return self.elderly_radii_distribubtion
    
    def _get_elderly_cell_information(self):
        return self.elderly_cell_information
    
    def _get_elderly_seed(self):
        return self.elderly_seed
 
    def _get_average_parameter_distributions(self):
        return self.average_parameter_distributions
    
    def _get_average_radii_distribution(self):
        return self.average_radii_distribution
    
    def _get_average_cell_information(self):
        return self.average_cell_information
    
    def _get_average_seed(self):
        return self.average_seed

class PopulationLog_Encoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, PopulationLog):
            return super(PopulationLog_Encoder, self).default(obj)

        return obj.__dict__

class PopulationLog_Decoder(json.JSONDecoder):
    def decode(self,json_string):
     
        default_obj = super(PopulationLog_Decoder,self).decode(json_string)

        children_num = default_obj['children_num']
        adult_num = default_obj['adult_num']
        elderly_num = default_obj['elderly_num']
        
        """ for children information """
        str_children_dist = default_obj['children_parameter_distributions']
        childrent_dist = json.loads(str_children_dist, cls =ChildrenLog_Decoder)   

        
        children_radii_distribution = []
        for radius in default_obj['children_radii_distribution']:
            children_radii_distribution.append(radius)
        
        children_cell_information = []
        for cell in default_obj['children_cell_information']:
            children_cell_information.append((cell[0],cell[1],cell[2]))
               
        children_seed = default_obj['children_seed']
        
        """ for adult information """
        str_adult_dist = default_obj['adult_parameter_distributions']
        adult_dist = json.loads(str_adult_dist, cls =AdultLog_Decoder)   
         
        adult_radii_distribution = []
        for radius in default_obj['adult_radii_distribution']:
            adult_radii_distribution.append(radius)
        
 
        adult_cell_information = []
        for cell in default_obj['adult_cell_information']:
            adult_cell_information.append((cell[0],cell[1],cell[2]))
        
        adult_seed = default_obj['adult_seed']
        
        """ for elderly information """
        str_elderly_dist = default_obj['elderly_parameter_distributions']
        elderly_dist = json.loads(str_elderly_dist, cls =ElderlyLog_Decoder)   
      
        elderly_radii_distribubtion = []
        for radius in default_obj['elderly_radii_distribubtion']:
            elderly_radii_distribubtion.append(radius)
        
        elderly_cell_information = []
        for cell in default_obj['elderly_cell_information']:
            elderly_cell_information.append((cell[0],cell[1],cell[2]))
            
        elderly_seed = default_obj['elderly_seed']
        
        """ for average information """
        str_average_dist = default_obj['average_parameter_distributions']
        average_dist = json.loads(str_average_dist, cls =AverageLog_Decoder)   
      
        average_radii_distribution = []
        for radius in default_obj['average_radii_distribution']:
            average_radii_distribution.append(radius)
            
        average_cell_information = []
        for cell in default_obj['average_cell_information']:
            average_cell_information.append((cell[0],cell[1],cell[2]))

        average_seed =  default_obj['average_seed']
        
        
        populationLog = PopulationLog(children_num,
                                      adult_num,
                                      elderly_num,
                 
                                      childrent_dist,
                                      children_radii_distribution,
                                      children_cell_information,                
                                      children_seed,
                 
                                      adult_dist,
                                      adult_radii_distribution,
                                      adult_cell_information,
                                      adult_seed,
                 
                                      elderly_dist,
                                      elderly_radii_distribubtion,
                                      elderly_cell_information,
                                      elderly_seed,
                 
                                      average_dist,
                                      average_radii_distribution,
                                      average_cell_information,
                                      average_seed)
        return populationLog                    