'''
Created on 16 Feb 2015

@author: quangv
'''
from pygame_drawing.scenario import Scenario

scenarios = {
        'bottleneckbiodirec': Scenario({
            'name'                          : 'bottleneck-bio',
            
            'average_num'                     : 2,
            ################################## for average pedestrian ##############################################################
            'average_velocity_mean'                 : [0.8,0.8], 
                          
            'average_force_unit'                    : [2.0,2.0],
         
                        
            ################################## for information the same between pedestrian types ##################################
            'start_areas'                         : [
                                                     (-30.0,-2.0), #[x1,x2]
                                                     (2.0,30.0),#[x3,x4] in 1 dimension
                                                    ],
            'targets'                             : [
                                                     (0.0),
                                                    ],   
            'drawing_width'                       : 1600,
            'drawing_height'                      : 850,
            'pixel_factor'                        : 23,
        })
}