'''
Created on 16 Feb 2015

@author: quangv
'''
from pygame_drawing.scenario import Scenario

scenarios = {
        'corridorunidirec': Scenario({
            'name'                    : 'corridor-uni',      
            'group_num'            : 50,                 
            ################################## for young pedestrian ##############################################################    
            'interaction_force'       : [1.0, 1.0], #3.0
            'interaction_force_step'  :  0.2,
             
            'interaction_range'       : [0.3,0.3], #2.0
            'interaction_range_step'  : 0.2,
                           
            'attraction_force'        : [1.0, 1.0], #3.0
            'attraction_force_step'   :  0.2,
             
            'attraction_range'        : [0.2,0.2], #2.0
            'attraction_range_step'   : 0.2,  
             
            ################################## for information of environment and shared parameters ##################################                
            'radius_mean'                         : 0.3,
            'radius_deviation'                    : 0.00,
          
            'start_areas'                         : [
                                                     (-10.5,-10.5,10.5,10.5),
                                                     #(-4.5,-4.5,4.5,4.5),
                                                    ],
            'drawing_width'                       : 1300,
            'drawing_height'                      : 850,
            'pixel_factor'                        : 22,
        })
}