'''
Created on 23 Apr 2015

@author: quangv
'''
import json

from src.pedestrian_types.average import AverageLog_Decoder

class PopulationLog(object):
    
    def __init__(self, 
                 average_num,                 
                 average_parameter_distributions,
                 average_cell_information):
        self.average_num = average_num
      
        self.average_parameter_distributions = average_parameter_distributions
        self.average_cell_information = average_cell_information      
        
    def _get_average_num(self):
        return self.average_num
 
    def _get_average_parameter_distributions(self):
        return self.average_parameter_distributions
    
    def _get_average_cell_information(self):
        return self.average_cell_information
  

class PopulationLog_Encoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, PopulationLog):
            return super(PopulationLog_Encoder, self).default(obj)

        return obj.__dict__

class PopulationLog_Decoder(json.JSONDecoder):
    def decode(self,json_string):
     
        default_obj = super(PopulationLog_Decoder,self).decode(json_string)

        average_num = default_obj['average_num']
        
        """ for average information """
        str_average_dist = default_obj['average_parameter_distributions']
        average_dist = json.loads(str_average_dist, cls =AverageLog_Decoder)   
    
        average_cell_information = []
        for cell in default_obj['average_cell_information']:
            average_cell_information.append((cell[0],cell[1]))
    
        populationLog = PopulationLog(average_num,
                                      average_dist,
                                      average_cell_information)
        return populationLog                    