'''
Created on 16 Feb 2015

@author: quangv
'''
from pygame_drawing.scenario import Scenario

scenarios = {
        'corridorunidirec': Scenario({
            'name'                    : 'corridor-uni',          

            'group'                   : 2,
            
            'group_num'               : [50,50],
            
            'group_id'                : [0,1], #it should start from 0
                      
            'in_group_r_strength'        : 40,          
            'in_group_r_range'        : 2.0,
            'in_group_a_strength'        : 20,
            'in_group_a_range'        : 2.80,
            
            'out_group_r_strength'        :40,
            'out_group_r_range'        :2.0,
            'out_group_a_strength'       : 20,
            'out_group_a_range'       : 2.80,
            
            'radius_mean'                         : 0.3,
     
            'start_areas'                         : [
                                                     (-14.5,-14.5,14.5,14.5),
                                                    ],
                                                                   
            'drawing_width'                       : 1300,
            'drawing_height'                      : 900,
            'pixel_factor'                        : 23,
        })
}