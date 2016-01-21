'''
Created on 16 Feb 2015

@author: quangv
'''
from pygame_drawing.scenario import Scenario

scenarios = {
        'corridorunidirec': Scenario({
            'name'                    : 'corridor-uni',      
            'group_num'            : 2,                 
            ################################## for young pedestrian ##############################################################    
            'interaction_force'       : 2.5, #2.5
            
            'interaction_range'       : 0.3,
                           
            'attraction_force'        : 1.0,#1.0,#1.0#0.5,
             
            'attraction_range'        : 0.8,#0.8
              
             
            ################################## for information of environment and shared parameters ##################################                
            'radius_mean'                         : 0.3,
        
            'start_areas'                         : [
                                                     (-1.5,1.5)],
            'drawing_width'                       : 1300,
            'drawing_height'                      : 850,
            'pixel_factor'                        : 22,
        })
}