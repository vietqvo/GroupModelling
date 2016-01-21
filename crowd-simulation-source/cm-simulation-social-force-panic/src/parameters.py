'''
Created on 16 Feb 2015

@author: quangv
'''
from pygame_drawing.scenario import Scenario

scenarios = {
        'bottleneckunidirec': Scenario({
            'name'                          : 'bottleneck-uni',
            
            'young_num'                     : 24,
            'adult_num'                     : 23,
            'elderly_num'                   : 23,
                   
            ################################## for young pedestrian ##############################################################
            'young_velocity_mean'                 : 1.7, 
            'young_velocity_deviation'            : 0.17, 
                
            'young_relaxation_mean'               : 1.3, 
            'young_relaxation_deviation'          : 0.13, 
                
            'young_force_unit'                    : 4.0,
            'young_force_deviation'               : 0.40,
              
            'young_force_range'                   : 0.13, # decrease 50%
            'young_range_deviation'               : 0.013, 
          
            ################################## for adult pedestrian ###############################################################
            'adult_velocity_mean'                 : 1.3, # commonly used as Helbing, 2005
            'adult_velocity_deviation'            : 0.13,
                
            'adult_relaxation_mean'               : 1.0, #commonly used (Helbing, 2005)
            'adult_relaxation_deviation'          : 0.1, #10% percent as Nomad calibration from mean and its std
                
            'adult_force_unit'                    : 3.0,
            'adult_force_deviation'               : 0.3,
                
            'adult_force_range'                   : 0.3,# increase 50%
            'adult_range_deviation'               : 0.03,
                
            ################################## for elderly pedestrian #############################################################
            'elderly_velocity_mean'               : 0.9,
            'elderly_velocity_deviation'          : 0.09,
                
            'elderly_relaxation_mean'             : 0.5,
            'elderly_relaxation_deviation'        : 0.05,
                
            'elderly_force_unit'                  : 2.0,
            'elderly_force_deviation'             : 0.2,
                        
            'elderly_force_range'                 : 0.2,
            'elderly_range_deviation'             : 0.02,
            
            
            ################################## for information the same between pedestrian types ##################################
            'max_velocity_factor'                 : 1.3,
                
            'radius_mean'                         : 0.3,
            'radius_deviation'                    : 0.05,
                
            'lambda'                              : 0.75,
                
            'U'                                   : 5.0,
            'start_areas'                         : [
                                                     (-28.0,-3.5,-15.0,3.5),
                                                    ],
            'targets'                             : [
                                                     (-1.0,0.0),
                                                    ],   
            'walls'                               : [
                                                     (-28.0, 4.0, -2.0,  4.0),
                                                     (-28.0,-4.0, -2.0, -4.0),
                                                     (-2.0, 0.5, -2.0,  4.0),
                                                     (-2.0, -0.5, -2.0, -4.0),                                                     
                                                    ],
            'force_tracking_areas'                : [
                                                     (-5.0,4.0,-2.0,-4.0),
                                                    ],
            'drawing_width'                       : 1300,
            'drawing_height'                      : 850,
            'pixel_factor'                        : 23,
        })
}