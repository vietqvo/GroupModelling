'''
Created on 16 Feb 2015

@author: quangv
'''
from pygame_drawing.scenario import Scenario

scenarios = {
        'corridorunidirec': Scenario({
            'name'                    : 'corridor-uni',
            
            
            'group_num'            : 5,
                  
    ################################## for young pedestrian ##############################################################
            'velocity_mean'           : [1.0,1.0], #3.0
            'velocity_step'           :  0.2,
              
            'relaxation_mean'         : [0.2,0.2], #2.0  
            'relaxation_step'         :  0.2,
                
            'interaction_force'       : [1.0, 4.0], #3.0
            'interaction_force_step'  :  0.2,
             
            'interaction_range'       : [0.2,0.2], #2.0
            'interaction_range_step'  : 0.2,
                           
            'attraction_force'        : [1.0, 4.0], #3.0
            'attraction_force_step'   :  0.2,
             
            'attraction_range'        : [0.2,0.2], #2.0
            'attraction_range_step'   : 0.2,  
              
            ################################## for information of environment and shared parameters ##################################
            'max_velocity_factor'                 : 1.3,
                
            'radius_mean'                         : 0.3,
            'radius_deviation'                    : 0.00,
                
            'U'                                   : 5.0,
          
            'start_areas'                         : [
                                                     (-28.0,-3.5,-21.0,3.5),
                                                    ],
            'targets'                             : [
                                                     (10.0,0.0),
                                                    ],   
            'walls'                               : [ 
                                                     (-28.0, 4.0, 11.0,  4.0),
                                                     (-28.0,-4.0, 11.0, -4.0),                                                   
                                                    ],
            'drawing_width'                       : 1300,
            'drawing_height'                      : 850,
            'pixel_factor'                        : 23,
        })
}