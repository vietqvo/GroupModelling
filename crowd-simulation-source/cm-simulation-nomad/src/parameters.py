'''
Created on 16 Feb 2015

@author: quangv
'''
from scenario import Scenario

scenarios = {
        'unidirection': Scenario({
            'name'                          : 'unidirection',
            
            'young_num'                     :24,
            'adult_num'                     :48,
            'elderly_num'                   :8,
                   
            ################################## for young pedestrian ##############################################################
            'young_velocity_mean'                 : 1.04,
            'young_velocity_deviation'            : 0.05,
                
            'young_relaxation_mean'               : 2.44,
            'young_relaxation_deviation'          : 0.60,
                
            'young_force_unit'                    : 0.90,
            'young_force_deviation'               : 0.00,
              
            'young_force_range'                   : 0.48,
            'young_range_deviation'               : 0.12,
          
            ################################## for adult pedestrian ###############################################################
            'adult_velocity_mean'                 : 1.00,
            'adult_velocity_deviation'            : 0.06,
                
            'adult_relaxation_mean'               : 2.31,
            'adult_relaxation_deviation'          : 0.46,
                
            'adult_force_unit'                    : 0.63,
            'adult_force_deviation'               : 0.00,
                
            'adult_force_range'                   : 0.52,
            'adult_range_deviation'               : 0.10,
                
            ################################## for elderly pedestrian #############################################################
            'elderly_velocity_mean'               : 0.98,
            'elderly_velocity_deviation'          : 0.03,
                
            'elderly_relaxation_mean'             : 2.08,
            'elderly_relaxation_deviation'        : 0.27,
                
            'elderly_force_unit'                  : 0.52,
            'elderly_force_deviation'             : 0.00,
                        
            'elderly_force_range'                 : 0.49,
            'elderly_range_deviation'             : 0.06,
            
            ################################## for information the same between pedestrian types ##################################
                
            'radius_mean'                         : 0.3,
            'radius_deviation'                    : 0.05,
     
            'start_areas'                         : [
                                                     (-28.0,-3.5,-15.0,3.5),
                                                    ],
            'targets'                             : [
                                                     (3.0,0.0)
                                                    ],   
            'drawing_width'                       : 1300,
            'drawing_height'                      : 850,
            'pixel_factor'                        : 20,
             
            ############################## for flow rate #######################################################                         
            'flowrate_line'                       : (-10.0, -3.0, 3.0, 0.0),
        }),
                  
        'bidirection': Scenario({
            'name'                          : 'bidirection',
            
            'young_num'                     : 42,
            'adult_num'                     : 84,
            'elderly_num'                   : 14,
             
            ################################## for young pedestrian ##############################################################
            'young_velocity_mean'                 : 1.04,
            'young_velocity_deviation'            : 0.05,
                
            'young_relaxation_mean'               : 2.44,
            'young_relaxation_deviation'          : 0.60,
                
            'young_force_unit'                    : 0.9,
            'young_force_deviation'               : 0.0,#2.20,
              
            'young_force_range'                   : 0.48,
            'young_range_deviation'               : 0.12,
          
            ################################## for adult pedestrian ###############################################################
            'adult_velocity_mean'                 : 1.00,
            'adult_velocity_deviation'            : 0.06,
                
            'adult_relaxation_mean'               : 2.31,
            'adult_relaxation_deviation'          : 0.46,
                
            'adult_force_unit'                    : 0.63,
            'adult_force_deviation'               : 0.0,#1.23,
                
            'adult_force_range'                   : 0.52,
            'adult_range_deviation'               : 0.10,
                
            ################################## for elderly pedestrian #############################################################
            'elderly_velocity_mean'               : 0.98,
            'elderly_velocity_deviation'          : 0.03,
                
            'elderly_relaxation_mean'             : 2.08,
            'elderly_relaxation_deviation'        : 0.27,
                
            'elderly_force_unit'                  : 0.52,
            'elderly_force_deviation'             : 0.0,#0.13,
                        
            'elderly_force_range'                 : 0.49,
            'elderly_range_deviation'             : 0.06,
            ################################## for information the same between pedestrian types ##################################
            
            'radius_mean'                         : 0.3,
            'radius_deviation'                    : 0.05,
 
            'start_areas'                         : [
                                                     (-28.0,-3.5,-15.0,3.5),
                                                     (19.0,-3.5, 32.0,3.5),
                                                    ],
            'targets'                             : [
                                                     (32.0,0.0),
                                                     (-28.0,0.0),
                                                    ],   
            'drawing_width'                       : 1300,
            'drawing_height'                      : 850,
            'pixel_factor'                        : 20,
             
            ############################## for  flow rate #####################################################                             
            'flowrate_line'                       : (-11.0, -3.0, 11.0, 3.0),
        }),
}


#scenarios['unidirection'].run();

scenarios['bidirection'].run();