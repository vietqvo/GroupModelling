'''
Created on 13 Feb 2015

@author: quangv
'''

import json

from src import constants
from src.parameter_plots.distribution import DistributionPlot as distribution_plot
from src.pedestrian_types.adults import Adults as adults_group_distribution
from src.pedestrian_types.children import Children as children_group_distribution
from src.pedestrian_types.elderly import Elderly as elderly_group_distribution
from src.pedestrian_types.outgroup_peds import Outgroup_peds as outgroup_peds_distribution
from src.pedestrian_types.population_log import PopulationLog
from src.pedestrian_types.population_log import PopulationLog_Encoder


class PopulationGenerator:
    
    def __init__(self, parameters, 
                 outgroup_num, 
                 children_group_num, 
                 adults_group_num, 
                 elderly_group_num, 
                 quantification_plots, 
                 
                 children_velocity_mean,
                 children_relaxation_mean,
                 children_interaction_strength_mean,
                 children_interaction_range_mean,
                             
                 strTime):
        
        self.parameters = parameters
        
        self.outgroup_generated_pedestrians =[]
        self.group_generated_pedestrians = []
       
        self.outgroup_peds_dist = outgroup_peds_distribution(parameters)
        self.children_group_dist = children_group_distribution(parameters)
        self.adults_group_dist = adults_group_distribution(parameters)
        self.elderly_group_dist = elderly_group_distribution(parameters)
        
        
        if outgroup_num>0:
            self.outgroup_peds_dist._generate_outgroup_ped_normal_distribution(outgroup_num)
             
        if children_group_num >0:
            self.children_group_dist._generate_children_distribution(children_group_num,
                                                                     children_velocity_mean,
                                                                     children_relaxation_mean,
                                                                     children_interaction_strength_mean,
                                                                     children_interaction_range_mean)
        
        if adults_group_num >0:
            self.adults_group_dist._generate_adults_distribution(adults_group_num)
        
        if elderly_group_num >0:
            self.elderly_group_dist._generate_elderly_distribution(elderly_group_num)    
        
        
        self.total_population_num = children_group_num + adults_group_num + elderly_group_num + outgroup_num
        
        self.outgroup_num = outgroup_num
        self.children_group_num = children_group_num
        self.adults_group_num = adults_group_num
        self.elderly_group_num = elderly_group_num
        
        """ quantitative plotting """
        if quantification_plots ==True:
            quantitative_plot = distribution_plot(self.parameters)

            quantitative_plot._create_pedestrian_type_parameter_distribution_plot("Initial Desired Velocity", constants.quantification_plot_bin_num,
                                                                        ### for in-group information
                                                                        self.parameters['children_group_velocity_mean'], 
                                                                        self.parameters['children_group_velocity_deviation'],
                                                                        self.children_group_dist._get_children_desired_velocities_distribution(),
                                                                        
                                                                        self.parameters['adult_group_velocity_mean'], 
                                                                        self.parameters['adult_group_velocity_deviation'],
                                                                        self.adults_group_dist._get_adults_desired_velocities_distribution(),
                                                                        
                                                                        self.parameters['elderly_group_velocity_mean'],
                                                                        self.parameters['elderly_group_velocity_deviation'],
                                                                        self.elderly_group_dist._get_elderly_desired_velocities_distribution(),
                                                                        
                                                                        ### for out-group information
                                                                        self.parameters['outgroup_velocity_mean'],
                                                                        self.parameters['outgroup_velocity_deviation'],
                                                                        self.outgroup_peds_dist.get_outgroup_desired_velocities(),                                                                       
                                                                        strTime
                                                                        )
            

            quantitative_plot._create_pedestrian_type_parameter_distribution_plot("Relaxation Time", constants.quantification_plot_bin_num,
                                                                        ### for in group information
                                                                        self.parameters['children_group_relaxation_mean'],
                                                                        self.parameters['children_group_relaxation_deviation'],
                                                                        self.children_group_dist._get_children_relaxation_times_distribution(),
                                                                        
                                                                        self.parameters['adult_group_relaxation_mean'], 
                                                                        self.parameters['adult_group_relaxation_deviation'],
                                                                        self.adults_group_dist._get_adults_relaxation_times_distribution(),
                                                                        
                                                                        self.parameters['elderly_group_relaxation_mean'],
                                                                        self.parameters['elderly_group_relaxation_deviation'],
                                                                        self.elderly_group_dist._get_elderly_relaxation_times_distribution(),
                                                                        
                                                                        ### for out-group information
                                                                        self.parameters['outgroup_relaxation_mean'],
                                                                        self.parameters['outgroup_relaxation_deviation'],
                                                                        self.outgroup_peds_dist.get_outgroup_relaxation_times(),
                                                                        strTime
                                                                        )
            

            quantitative_plot._create_pedestrian_type_parameter_distribution_plot("Interaction Strength", constants.quantification_plot_bin_num,
                                                                        ### for in-group information
                                                                        self.parameters['children_group_force_unit'],
                                                                        self.parameters['children_group_force_deviation'],
                                                                        self.children_group_dist._get_children_interaction_strengths_distribution(),
                                                                         
                                                                        self.parameters['adult_group_force_unit'], 
                                                                        self.parameters['adult_group_force_deviation'],
                                                                        self.adults_group_dist._get_adults_interaction_strengths_distribution(),
                                                                        
                                                                        self.parameters['elderly_group_force_unit'],
                                                                        self.parameters['elderly_group_force_deviation'],
                                                                        self.elderly_group_dist._get_elderly_interaction_strengths_distribution(),
                                                                        
                                                                        ### for out-group information
                                                                        self.parameters['outgroup_force_unit'],
                                                                        self.parameters['outgroup_force_deviation'],
                                                                        self.outgroup_peds_dist.get_outgroup_interaction_strengths(),
                                                                        strTime 
                                                                        )
            
            
            quantitative_plot._create_pedestrian_type_parameter_distribution_plot("Interaction Range", constants.quantification_plot_bin_num,
                                                                        ### for in-group information
                                                                        self.parameters['children_group_force_range'],
                                                                        self.parameters['children_group_range_deviation'],
                                                                        self.children_group_dist._get_children_interaction_ranges_distribution(),
                                                                        
                                                                        self.parameters['adult_group_force_range'], 
                                                                        self.parameters['adult_group_range_deviation'],
                                                                        self.adults_group_dist._get_adults_interaction_ranges_distribution(),
                                                                        
                                                                        self.parameters['elderly_group_force_range'],
                                                                        self.parameters['elderly_group_range_deviation'],
                                                                        self.elderly_group_dist._get_elderly_interaction_ranges_distribution(),
                                                                        
                                                                         ### for out-group information
                                                                        self.parameters['outgroup_force_range'],
                                                                        self.parameters['outgroup_range_deviation'],
                                                                        self.outgroup_peds_dist.get_outgroup_interaction_ranges(),
                                                                        strTime
                                                                        )
                  
    def _generate_population(self,     
                             placement_radii_info,
                             placement_position_info):
  
        """ generate radii for all population """
        
        self.radii_for_young = placement_radii_info["radii_children"]
        self.radii_for_adult = placement_radii_info["radii_adults"]
        self.radii_for_elderly = placement_radii_info["radii_elders"]
        self.radii_for_out_group_peds = placement_radii_info["radii_outgroup"]
       
        self.position_children =placement_position_info["position_children"] 
        self.position_adults =placement_position_info["position_adults"] 
        self.position_elders =placement_position_info["position_elders"] 
        self.position_outgroup =placement_position_info["position_outgroup"] 
        
        self.generated_group_pedestrians = []
        self.generated_out_group_pedestrians = []
         
        """ check pedestrian_Id """
        self.generated_group_member_index = 0
        self.generated_out_group_pedestrian_index = self.children_group_num + self.adults_group_num  + self.elderly_group_num -1  ##index order 
        
        if self.children_group_num > 0:
         
            young_pedestrians= self._create_pedestrian_by_distribution(0, self.position_children, self.radii_for_young)
            self.generated_group_pedestrians.extend(young_pedestrians)
               
        if  self.adults_group_num >0:     
           
            adult_pedestrians = self._create_pedestrian_by_distribution(1, self.position_adults, self.radii_for_adult)
            self.generated_group_pedestrians.extend(adult_pedestrians)
        
        if self.elderly_group_num>0:
            elderly_pedestrians = self._create_pedestrian_by_distribution(2, self.position_elders, self.radii_for_elderly)
            self.generated_group_pedestrians.extend(elderly_pedestrians)
        
        if self.outgroup_num > 0:
            self.generated_out_group_pedestrians = self._create_pedestrian_by_distribution(3, self.position_outgroup, self.radii_for_out_group_peds)
     
    def _create_pedestrian_by_distribution(self, pes_type, designated_positions, radiis):

        pedestrians_in_same_type =[]
        velocities =[]
        relaxation_times =[]
        interaction_strengths = []
        interaction_ranges = []
                   
        
        if pes_type == 0: # young group member
            velocities = self.children_group_dist._get_children_desired_velocities_distribution()
            relaxation_times = self.children_group_dist._get_children_relaxation_times_distribution()
            interaction_strengths =  self.children_group_dist._get_children_interaction_strengths_distribution()
            interaction_ranges = self.children_group_dist._get_children_interaction_ranges_distribution()
    
        elif pes_type ==1: # adult group member
            velocities = self.adults_group_dist._get_adults_desired_velocities_distribution()
            relaxation_times = self.adults_group_dist._get_adults_relaxation_times_distribution()
            interaction_strengths =  self.adults_group_dist._get_adults_interaction_strengths_distribution()
            interaction_ranges = self.adults_group_dist._get_adults_interaction_ranges_distribution() 
                     
        elif pes_type == 2: # elderly group member
            velocities = self.elderly_group_dist._get_elderly_desired_velocities_distribution()
            relaxation_times = self.elderly_group_dist._get_elderly_relaxation_times_distribution()
            interaction_strengths =  self.elderly_group_dist._get_elderly_interaction_strengths_distribution()
            interaction_ranges = self.elderly_group_dist._get_elderly_interaction_ranges_distribution()
                 
        elif pes_type==3: # out-group people =3 
            velocities = self.outgroup_peds_dist.get_outgroup_desired_velocities()
            relaxation_times = self.outgroup_peds_dist.get_outgroup_relaxation_times()
            interaction_strengths =  self.outgroup_peds_dist.get_outgroup_interaction_strengths()
            interaction_ranges = self.outgroup_peds_dist.get_outgroup_interaction_ranges()
                                                         
        for i in range(len(designated_positions)):
      
            pedestrian_id = 0
            
            if pes_type ==0 or pes_type == 1 or pes_type == 2:
                self.generated_group_member_index+=1
                pedestrian_id = self.generated_group_member_index
            
            elif pes_type == 3:
                self.generated_out_group_pedestrian_index +=1
                pedestrian_id = self.generated_out_group_pedestrian_index
          
            pedestrians_in_same_type.append(dict(
                p_type = pes_type,
                pedestrian_id = pedestrian_id,
                
                position = designated_positions[i]['position'],
                radius = radiis[i],
                initial_position = designated_positions[i]['position'],
                
                acceleration = (0.0, 0.0),
                initial_desired_velocity = velocities[i],
                velocity = (0.0, 0.0),
                time = 0.0,
                relax_time = relaxation_times[i],
                max_velocity = velocities[i] * self.parameters['max_velocity_factor'],
                target = designated_positions[i]['target'],
                 
                force_unit = interaction_strengths[i],
                interaction_range = interaction_ranges[i],
                interaction_lamda = self.parameters['lambda'],
                
                desired_force_tracking = (0.0,0.0),
                interaction_force_tracking = (0.0,0.0),
                obstacle_force_tracking = (0.0,0.0)))
                   
        
        return pedestrians_in_same_type
    
    
    def _get_generated_group_pedestrians_population(self): 
        return self.generated_group_pedestrians
    
    def _get_generated_out_group_pedestrians_population(self): 
        return self.generated_out_group_pedestrians
    
  
    def _log_generation(self, log_dir):
        population_log =   PopulationLog(self.children_group_num,
                                         self.adults_group_num,
                                         self.elderly_group_num,
                                         self.outgroup_num,
                                         
                                         self.children_group_dist._to_JSON(),
                                         self.radii_for_young,
                                         self.position_children,
                                         
                                         self.adults_group_dist._to_JSON(),
                                         self.radii_for_adult,
                                         self.position_adults,
                                         
                                         self.elderly_group_dist._to_JSON(),
                                         self.radii_for_elderly,
                                         self.position_elders,
                                    
                                         self.outgroup_peds_dist._to_JSON(),
                                         self.radii_for_out_group_peds,
                                         self.position_outgroup
                                         )
        
        log_file = open( "%s.log" % log_dir, "w")

        json_obj = json.dumps(population_log, cls=PopulationLog_Encoder)
        log_file.write(json_obj)
        log_file.close()