'''
Created on 16 Feb 2015

@author: quangv
'''
from pygame_drawing.scenario import Scenario

scenarios = {
        'bottleneckbiodirec': Scenario({
            'name'                          : 'bottleneck-bio',
            
            'young_num'                     : 2,
            'elderly_num'                   : 1,
                   
            ################################## for young pedestrian ##############################################################
            'young_velocity_mean'                 : 0.8, 
            'young_velocity_deviation'            : 0.08, 
                          
            'young_force_unit'                    : 4.0,
            'young_force_deviation'               : 0.40,
                   
            ################################## for elderly pedestrian #############################################################
            'elderly_velocity_mean'               : 0.8,
            'elderly_velocity_deviation'          : 0.08,
                              
            'elderly_force_unit'                  : 2.0,
            'elderly_force_deviation'             : 0.2,
                        
            ################################## for information the same between pedestrian types ##################################
        
            'radius_mean'                         : 0.3,
            'radius_deviation'                    : 0.05,
            
            'start_areas'                         : [
                                                     (-31.0,-0.4,-2.0,0.4), #[x1,y1,x2,y2]
                                                     (2.0,-0.4,31.0,0.4),#[x3-x4] in 1 dimension
                                                    ],
            'targets'                             : [
                                                     (0.0),
                                                    ],   
            'main_axis'                           : [
                                                     (-28.0, 0.0, 28.0,  0.0),                                                 
                                                    ],
            'drawing_width'                       : 1600,
            'drawing_height'                      : 850,
            'pixel_factor'                        : 23,
        })
}