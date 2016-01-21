'''
Created on 16 Feb 2015

@author: quangv
'''
from pygame_drawing.scenario import Scenario

scenarios = {
        'corridorunidirec': Scenario({
            'name'                          : 'corridor-uni',
            
            'outgroup_num'                  : 0,
            
            'children_group_num'            : 4, #as Moussaid statistically //walk side by side, if then revert to V when densitiy increases
                                                #Assuming people have a 180° vision field
                                        
            'adult_group_num'               : 0,
            'elder_group_num'               : 0,
            
                  
            ################################## for out group pedestrian ##############################################################
            'outgroup_velocity_mean'                 : 1.3, 
            'outgroup_velocity_deviation'            : 0.0, 
                
            'outgroup_relaxation_mean'               : 0.5, 
            'outgroup_relaxation_deviation'          : 0.0, 
                
            'outgroup_force_unit'                    : 3.0,
            'outgroup_force_deviation'               : 0.0,
              
            'outgroup_force_range'                   : 0.2,
            'outgroup_range_deviation'               : 0.0, 
          
            ################################## for young pedestrian ##############################################################
            'children_group_velocity_mean'           : [2.2,2.2],# range of possible data from Helbing [1.0,3.0]
            #'children_group_velocity_mean'          : 1.3,
            'children_group_velocity_step'           :  0.2,
            'children_group_velocity_deviation'      : 0.0, 
                
              
            'children_group_relaxation_mean'         : [0.2,0.2],# range of possible data from Helbing  [0.2,2.0]   
            #'children_group_relaxation_mean'        : 0.5,
            'children_group_relaxation_step'           :  0.2,
            'children_group_relaxation_deviation'    : 0.0, 
                
                
            'children_group_force_unit'              : [1.0, 1.0], #possible data from Helbing [1.0, 4.0]
            'children_group_force_step'              :  0.2,
            #'children_group_force_unit'             :3.0,
            'children_group_force_deviation'         : 0.0,
              
             
            'children_group_force_range'             : [0.2,0.2], #possible data range from Helbing [0.2,2.0]
            #'children_group_force_range'             : 0.2,
            'children_group_range_step'              : 0.2,  
            'children_group_range_deviation'         : 0.0, 
          
            ################################## for adult pedestrian ###############################################################
            'adult_group_velocity_mean'              : 1.3, 
            'adult_group_velocity_deviation'         : 0.0,
                
            'adult_group_relaxation_mean'               : 0.5, 
            'adult_group_relaxation_deviation'          : 0.0, 
                
            'adult_group_force_unit'                    : 3.0,
            'adult_group_force_deviation'               : 0.0,
                
            'adult_group_force_range'                   : 0.2,
            'adult_group_range_deviation'               : 0.0,
                
            ################################## for elderly pedestrian #############################################################
            'elderly_group_velocity_mean'               : 1.3,
            'elderly_group_velocity_deviation'          : 0.0,
                
            'elderly_group_relaxation_mean'             : 0.5,
            'elderly_group_relaxation_deviation'        : 0.0,
                
            'elderly_group_force_unit'                  : 3.0,
            'elderly_group_force_deviation'             : 0.0,
                        
            'elderly_group_force_range'                 : 0.2,
            'elderly_group_range_deviation'             : 0.0,
            
            
            ################################## for information of environment and shared parameters ##################################
            'max_velocity_factor'                 : 1.3,
                
            'radius_mean'                         : 0.3,
            'radius_deviation'                    : 0.05,
                
            'lambda'                              : 0.75,
                
            'U'                                   : 5.0,
            'group_force_beta1'                   : 4.0,
            
            'group_force_alpha_model'             : 0.17, #ped turn 0.08 = 10 degree head to make sure center of mass in his vision field
            
            'group_force_beta2'                   : 0.5,#cohesion force if the distance between this group member and center of mass is large then (N-1)/2 meter
            
            'group_force_distance_repulsion_effect': 0.5,#distance threshold for computing repulsion between this two group members 
            
            'group_force_beta3'                   : 0.5,#repulsion effect unit 0.3
            
            'start_areas'                         : [
                                                     #(-28.0,-3.5,-18.0,3.5),
                                                     (-28.0,-2,-24.0,2),
                                                    ],
            'targets'                             : [
                                                     (10.0,0.0),
                                                    ],   
            'walls'                               : [
                                                     #(-28.0, 2.0, 11.0,  2.0),
                                                     #(-28.0,-2.0, 11.0, -2.0),    
                                                     (-28.0, 4.0, 11.0,  4.0),
                                                     (-28.0,-4.0, 11.0, -4.0),                                                   
                                                    ],
            'drawing_width'                       : 1300,
            'drawing_height'                      : 850,
            'pixel_factor'                        : 23,
        })
}