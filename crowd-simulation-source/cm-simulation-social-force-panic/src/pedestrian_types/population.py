'''
Created on 13 Feb 2015

@author: quangv
'''

import numpy, math, random
from datetime import datetime
import json

from src import constants
from src.parameter_plots.distribution import DistributionPlot as distribution_plot
from src.pedestrian_types.adults import Adults as adults_distribution
from src.pedestrian_types.children import Children as children_distribution
from src.pedestrian_types.elderly import Elderly as elderly_distribution
from src.pedestrian_types.average import Average as average_distribution
from src.pedestrian_types.population_log import PopulationLog
from src.pedestrian_types.population_log import PopulationLog_Encoder


class PopulationGenerator:
    
    def __init__(self, parameters, children_num, adults_num, elderly_num, quantification_plots, strTime):
        self.parameters = parameters
        
        self.different_generated_pedestrians =[]
        self.average_generated_pedestrians = []
       
        self.children_dist = children_distribution(parameters)
        self.adults_dist = adults_distribution(parameters)
        self.elderly_dist = elderly_distribution(parameters)
        self.average_dist = average_distribution(parameters)
 
        
        if children_num >0:
            self.children_dist._generate_children_distribution(children_num)
        
        if adults_num >0:
            self.adults_dist._generate_adults_distribution(adults_num)
        
        if elderly_num >0:
            self.elderly_dist._generate_elderly_distribution(elderly_num)    
        
        self.total_population_num = children_num + adults_num + elderly_num
        self.young_num = children_num
        self.adults_num = adults_num
        self.elderly_num = elderly_num
        
        """ get all desired_velocities of three pedestrian types"""
        desired_velocities =  []
        desired_velocities += self.children_dist._get_children_desired_velocities_distribution()
        desired_velocities += self.adults_dist._get_adults_desired_velocities_distribution()
        desired_velocities += self.elderly_dist._get_elderly_desired_velocities_distribution()
        
        """ get all relaxation times of three pedestrian types"""
        relaxation_times = []
        relaxation_times += self.children_dist._get_children_relaxation_times_distribution()
        relaxation_times += self.adults_dist._get_adults_relaxation_times_distribution()
        relaxation_times += self.elderly_dist._get_elderly_relaxation_times_distribution()
        
        """ get all interaction strengths of three pedestrian types"""
        interaction_strengths =[]
        interaction_strengths += self.children_dist._get_children_interaction_strengths_distribution()
        interaction_strengths += self.adults_dist._get_adults_interaction_strengths_distribution()
        interaction_strengths += self.elderly_dist._get_elderly_interaction_strengths_distribution()
        
        """ get all interaction ranges of three pedestrian types"""
        interaction_ranges =[]
        interaction_ranges += self.children_dist._get_children_interaction_ranges_distribution()
        interaction_ranges += self.adults_dist._get_adults_interaction_ranges_distribution()
        interaction_ranges += self.elderly_dist._get_elderly_interaction_ranges_distribution()
        
        
        """ get mean low level and high level of each parameter """
        children_desired_velocities_mean = numpy.mean(self.children_dist._get_children_desired_velocities_distribution())
        adults_desired_velocities_mean = numpy.mean(self.adults_dist._get_adults_desired_velocities_distribution())
        elders_desired_velocities_mean = numpy.mean(self.elderly_dist._get_elderly_desired_velocities_distribution())                                           
        min_desired_velocity_value = min(children_desired_velocities_mean, adults_desired_velocities_mean, elders_desired_velocities_mean)   
        max_desired_velocity_value = max(children_desired_velocities_mean, adults_desired_velocities_mean, elders_desired_velocities_mean)
                                                   
        children_relaxation_times_mean= numpy.mean(self.children_dist._get_children_relaxation_times_distribution())
        adults_relaxation_times_mean = numpy.mean(self.adults_dist._get_adults_relaxation_times_distribution())
        elders_relaxation_times_mean = numpy.mean(self.elderly_dist._get_elderly_relaxation_times_distribution())
        min_relaxation_time_value = min(children_relaxation_times_mean, adults_relaxation_times_mean, elders_relaxation_times_mean)    
        max_relaxation_time_value = max(children_relaxation_times_mean, adults_relaxation_times_mean, elders_relaxation_times_mean)  
      
        children_interaction_strengths_mean =  numpy.mean(self.children_dist._get_children_interaction_strengths_distribution())
        adults_interaction_strengths_mean = numpy.mean(self.adults_dist._get_adults_interaction_strengths_distribution())
        elders_interaction_strengths_mean = numpy.mean(self.elderly_dist._get_elderly_interaction_strengths_distribution())
        min_interaction_strengths_value = min(children_interaction_strengths_mean, adults_interaction_strengths_mean, elders_interaction_strengths_mean)    
        max_interaction_strengths_value = max(children_interaction_strengths_mean, adults_interaction_strengths_mean, elders_interaction_strengths_mean)
                                                                                                                                    
         
        children_interaction_ranges_mean = numpy.mean(self.children_dist._get_children_interaction_ranges_distribution())
        adults_interaction_ranges_mean = numpy.mean(self.adults_dist._get_adults_interaction_ranges_distribution())                                                                        
        elders_interaction_ranges_mean = numpy.mean(self.elderly_dist._get_elderly_interaction_ranges_distribution())                                                                        
        min_interaction_ranges_value = min(children_interaction_ranges_mean, adults_interaction_ranges_mean, elders_interaction_ranges_mean) 
        max_interaction_ranges_value = max(children_interaction_ranges_mean, adults_interaction_ranges_mean, elders_interaction_ranges_mean) 
        
              
        if self.total_population_num >0:
            self.average_dist._generate_average_normal_distribution(numpy.mean(desired_velocities), numpy.std(desired_velocities), 
                                                            numpy.mean(relaxation_times), numpy.std(relaxation_times), 
                                                            numpy.mean(interaction_strengths), numpy.std(interaction_strengths), 
                                                            numpy.mean(interaction_ranges), numpy.std(interaction_ranges), 
                                                            self.total_population_num)
                                                      
            self.average_dist._generate_average_cutoff_level_normal_distribution(numpy.mean(desired_velocities), numpy.std(desired_velocities),
                                                                                min_desired_velocity_value,max_desired_velocity_value,
                                                                               
                                                                               numpy.mean(relaxation_times), numpy.std(relaxation_times),
                                                                               min_relaxation_time_value, max_relaxation_time_value,
                                                                               
                                                                               numpy.mean(interaction_strengths), numpy.std(interaction_strengths),
                                                                               min_interaction_strengths_value, max_interaction_strengths_value,
                                                                               
                                                                               numpy.mean(interaction_ranges), numpy.std(interaction_ranges),
                                                                               min_interaction_ranges_value, max_interaction_ranges_value,
                                                                               
                                                                               self.total_population_num, 3)
            
            self.average_dist._generate_average_cutoff_level_normal_distribution(numpy.mean(desired_velocities), numpy.std(desired_velocities),
                                                                                min_desired_velocity_value,max_desired_velocity_value,
                                                                               
                                                                               numpy.mean(relaxation_times), numpy.std(relaxation_times),
                                                                               min_relaxation_time_value,max_relaxation_time_value,
                                                                               
                                                                               numpy.mean(interaction_strengths), numpy.std(interaction_strengths),
                                                                               min_interaction_strengths_value, max_interaction_strengths_value,
                                                                               
                                                                               numpy.mean(interaction_ranges), numpy.std(interaction_ranges),
                                                                               min_interaction_ranges_value,max_interaction_ranges_value,
                                                                               
                                                                               self.total_population_num, 1)

            self.average_dist._generate_uniform_cutoff_level_distribution(min_desired_velocity_value,max_desired_velocity_value,
                                                                           min_relaxation_time_value,max_relaxation_time_value,
                                                                           min_interaction_strengths_value, max_interaction_strengths_value,
                                                                           min_interaction_ranges_value,max_interaction_ranges_value,
                                                                           self.total_population_num,3)
                  
            self.average_dist._generate_uniform_cutoff_level_distribution(min_desired_velocity_value,max_desired_velocity_value,
                                                                          min_relaxation_time_value,max_relaxation_time_value,
                                                                          min_interaction_strengths_value, max_interaction_strengths_value,
                                                                          min_interaction_ranges_value,max_interaction_ranges_value,
                                                                          self.total_population_num,1)
                        
        
        """ quantitative plotting """
        if quantification_plots ==True:
            quantitative_plot = distribution_plot(self.parameters)

            quantitative_plot._create_pedestrian_type_parameter_distribution_plot("Initial Desired Velocity", constants.quantification_plot_bin_num,
                                                                        ### for differential prototype
                                                                        self.parameters['young_velocity_mean'], 
                                                                        self.parameters['young_velocity_deviation'],
                                                                        self.children_dist._get_children_desired_velocities_distribution(),
                                                                        
                                                                        self.parameters['adult_velocity_mean'], 
                                                                        self.parameters['adult_velocity_deviation'],
                                                                        self.adults_dist._get_adults_desired_velocities_distribution(),
                                                                        
                                                                        self.parameters['elderly_velocity_mean'],
                                                                        self.parameters['elderly_velocity_deviation'],
                                                                        self.elderly_dist._get_elderly_desired_velocities_distribution(),
                                                                        
                                                                        ### for average prototype
                                                                        numpy.mean(desired_velocities), 
                                                                        numpy.std(desired_velocities),
                                                                        self.average_dist.get_average_desired_velocities(),
                                                                        
                                                                        ### for average cutoff_level 3_normal prototype
                                                                        numpy.mean(desired_velocities), 
                                                                        numpy.std(desired_velocities),                   
                                                                        self.average_dist.get_average_cutoff_lv_3_desired_velocities_low_value(),                                                                       
                                                                        self.average_dist.get_average_cutoff_lv_3_desired_velocities_high_value(),                                                                     
                                                                        self.average_dist.get_average_cutoff_lv_3_desired_velocities(),
                                                                        
                                                                        ### for average cutoff_level 1_normal prototype
                                                                        numpy.mean(desired_velocities),
                                                                        numpy.std(desired_velocities),                   
                                                                        self.average_dist.get_average_cutoff_lv_1_desired_velocities_low_value(),                                                                       
                                                                        self.average_dist.get_average_cutoff_lv_1_desired_velocities_high_value(),                                                                     
                                                                        self.average_dist.get_average_cutoff_lv_1_desired_velocities(),
                                                                        
                                                                        ### for uniform cutoff_level 3 prototype             
                                                                        self.average_dist.get_uniform_cutoff_lv_3_desired_velocities_low_value(),                                                                       
                                                                        self.average_dist.get_uniform_cutoff_lv_3_desired_velocities_high_value(),                                                                     
                                                                        self.average_dist.get_uniform_cutoff_lv_3_desired_velocities(),
                                                                        
                                                                        ### for uniform cutoff_level 1
                                                                        self.average_dist.get_uniform_cutoff_lv_1_desired_velocities_low_value(),                                                                       
                                                                        self.average_dist.get_uniform_cutoff_lv_1_desired_velocities_high_value(),                                                                     
                                                                        self.average_dist.get_uniform_cutoff_lv_1_desired_velocities(),
                                                                        strTime
                                                                        )
            

            quantitative_plot._create_pedestrian_type_parameter_distribution_plot("Relaxation Time", constants.quantification_plot_bin_num,
                                                                        ### for differential prototype
                                                                        self.parameters['young_relaxation_mean'],
                                                                        self.parameters['young_relaxation_deviation'],
                                                                        self.children_dist._get_children_relaxation_times_distribution(),
                                                                        
                                                                        self.parameters['adult_relaxation_mean'], 
                                                                        self.parameters['adult_relaxation_deviation'],
                                                                        self.adults_dist._get_adults_relaxation_times_distribution(),
                                                                        
                                                                        self.parameters['elderly_relaxation_mean'],
                                                                        self.parameters['elderly_relaxation_deviation'],
                                                                        self.elderly_dist._get_elderly_relaxation_times_distribution(),
                                                                        
                                                                        ### for average prototype
                                                                        numpy.mean(relaxation_times), 
                                                                        numpy.std(relaxation_times),
                                                                        self.average_dist.get_average_relaxation_times(),
                                                                        
                                                                        ### for average cutoff_level 3_normal prototype
                                                                        numpy.mean(relaxation_times), 
                                                                        numpy.std(relaxation_times),                   
                                                                        self.average_dist.get_average_cutoff_lv_3_relaxation_times_low_value(),                                                                       
                                                                        self.average_dist.get_average_cutoff_lv_3_relaxation_times_high_value(),                                                                     
                                                                        self.average_dist.get_average_cutoff_lv_3_relaxation_times(),

                                                                        ### for average cutoff_level 1_normal prototype
                                                                        numpy.mean(relaxation_times), 
                                                                        numpy.std(relaxation_times),      
                                                                        self.average_dist.get_average_cutoff_lv_1_relaxation_times_low_value(),
                                                                        self.average_dist.get_average_cutoff_lv_1_relaxation_times_high_value(),
                                                                        self.average_dist.get_average_cutoff_lv_1_relaxation_times(),
                                                                        
                                                                        ### for uniform cutoff_level 3 prototype  
                                                                        self.average_dist.get_uniform_cutoff_lv_3_relaxation_times_low_value(),
                                                                        self.average_dist.get_uniform_cutoff_lv_3_relaxation_times_high_value(),
                                                                        self.average_dist.get_uniform_cutoff_lv_3_relaxation_times(),
                                                                        
                                                                        ### for uniform cutoff_level 1 prototype
                                                                        self.average_dist.get_uniform_cutoff_lv_1_relaxation_times_low_value(),
                                                                        self.average_dist.get_uniform_cutoff_lv_1_relaxation_times_high_value(),
                                                                        self.average_dist.get_uniform_cutoff_lv_1_relaxation_times(),
                                                                        strTime
                                                                        )
            

            quantitative_plot._create_pedestrian_type_parameter_distribution_plot("Interaction Strength", constants.quantification_plot_bin_num,
                                                                        ### for differential prototype
                                                                        self.parameters['young_force_unit'],
                                                                        self.parameters['young_force_deviation'],
                                                                        self.children_dist._get_children_interaction_strengths_distribution(),
                                                                         
                                                                        self.parameters['adult_force_unit'], 
                                                                        self.parameters['adult_force_deviation'],
                                                                        self.adults_dist._get_adults_interaction_strengths_distribution(),
                                                                        
                                                                        self.parameters['elderly_force_unit'],
                                                                        self.parameters['elderly_force_deviation'],
                                                                        self.elderly_dist._get_elderly_interaction_strengths_distribution(),
                                                                        
                                                                        ### for average prototype
                                                                        numpy.mean(interaction_strengths), 
                                                                        numpy.std(interaction_strengths),   
                                                                        self.average_dist.get_average_interaction_strengths(),
                                                                        
                                                                        ### for average cutoff_level 3_normal prototype
                                                                        numpy.mean(interaction_strengths), 
                                                                        numpy.std(interaction_strengths),                    
                                                                        self.average_dist.get_average_cutoff_lv_3_interaction_strengths_low_value(),                                                                       
                                                                        self.average_dist.get_average_cutoff_lv_3_interaction_strengths_high_value(),                                                                     
                                                                        self.average_dist.get_average_cutoff_lv_3_interaction_strengths(),

                                                                        ### for average cutoff_level 1_normal prototype
                                                                        numpy.mean(interaction_strengths), 
                                                                        numpy.std(interaction_strengths),                    
                                                                        self.average_dist.get_average_cutoff_lv_1_interaction_strengths_low_value(),                                                                       
                                                                        self.average_dist.get_average_cutoff_lv_1_interaction_strengths_high_value(),                                                                     
                                                                        self.average_dist.get_average_cutoff_lv_1_interaction_strengths(),
                                                                        
                                                                        ### for uniform cutoff_level 3_normal prototype                  
                                                                        self.average_dist.get_uniform_cutoff_lv_3_interaction_strengths_low_value(),                                                                       
                                                                        self.average_dist.get_uniform_cutoff_lv_3_interaction_strengths_high_value(),                                                                     
                                                                        self.average_dist.get_uniform_cutoff_lv_3_interaction_strengths(),
                                                                        
                                                                        ### for uniform cutoff_level 1_normal prototype
                                                                        self.average_dist.get_uniform_cutoff_lv_1_interaction_strengths_low_value(),
                                                                        self.average_dist.get_uniform_cutoff_lv_1_interaction_strengths_high_value(),
                                                                        self.average_dist.get_uniform_cutoff_lv_1_interaction_strengths(),
                                                                        strTime 
                                                                        )
            
            
            quantitative_plot._create_pedestrian_type_parameter_distribution_plot("Interaction Range", constants.quantification_plot_bin_num,
                                                                        ### differential prototype
                                                                        self.parameters['young_force_range'],
                                                                        self.parameters['young_range_deviation'],
                                                                        self.children_dist._get_children_interaction_ranges_distribution(),
                                                                        
                                                                        self.parameters['adult_force_range'], 
                                                                        self.parameters['adult_range_deviation'],
                                                                        self.adults_dist._get_adults_interaction_ranges_distribution(),
                                                                        
                                                                        self.parameters['elderly_force_range'],
                                                                        self.parameters['elderly_range_deviation'],
                                                                        self.elderly_dist._get_elderly_interaction_ranges_distribution(),
                                                                        
                                                                        ### average prototype
                                                                        numpy.mean(interaction_ranges), 
                                                                        numpy.std(interaction_ranges),
                                                                        self.average_dist.get_average_interaction_ranges(),
                                                                        
                                                                        ### for average cutoff_level 3_normal prototype
                                                                        numpy.mean(interaction_ranges), 
                                                                        numpy.std(interaction_ranges),
                                                                        self.average_dist.get_average_cutoff_lv_3_interaction_ranges_low_value(),
                                                                        self.average_dist.get_average_cutoff_lv_3_interaction_ranges_high_value(),
                                                                        self.average_dist.get_average_cutoff_lv_3_interaction_ranges(),
                                                                        
                                                                        ### for average cutoff_level 1_normal prototype
                                                                        numpy.mean(interaction_ranges), 
                                                                        numpy.std(interaction_ranges),
                                                                        self.average_dist.get_average_cutoff_lv_1_interaction_ranges_low_value(),
                                                                        self.average_dist.get_average_cutoff_lv_1_interaction_ranges_high_value(),
                                                                        self.average_dist.get_average_cutoff_lv_1_interaction_ranges(),
                                                                      
                                                                        ### for uniform cutoff_level 3_normal prototype    
                                                                        self.average_dist.get_uniform_cutoff_lv_3_interaction_ranges_low_value(),
                                                                        self.average_dist.get_uniform_cutoff_lv_3_interaction_ranges_high_value(),
                                                                        self.average_dist.get_uniform_cutoff_lv_3_interaction_ranges(),
                                                                        
                                                                        ### for uniform cutoff_level 1_normal prototype
                                                                        self.average_dist.get_uniform_cutoff_lv_1_interaction_ranges_low_value(),
                                                                        self.average_dist.get_uniform_cutoff_lv_1_interaction_ranges_high_value(),
                                                                        self.average_dist.get_uniform_cutoff_lv_1_interaction_ranges(),
                                                                        strTime
                                                                        )
                  
    def _generate_population(self, start_areas,log_generation):
  
        """ generate radii for all population """
        radiis = []
       
        self.different_generated_pedestrians = []
        self.average_generated_pedestrians = []
        self.average_cutoff_lv3_generated_pedestrians = []
        self.average_cutoff_lv1_generated_pedestrians = []
        self.uniform_cutoff_lv3_generated_pedestrians = []
        self.uniform_cutoff_lv1_generated_pedestrians = []
        

        if self.parameters['radius_deviation'] > 0.0:
            while len(radiis) < self.total_population_num:
                samples = numpy.random.normal(self.parameters['radius_mean'],self.parameters['radius_deviation'], self.total_population_num)           
                radiis.extend(constants._filter_samples_by_mean(samples, self.total_population_num-len(radiis)))          

            max_radius = max(radiis)
        else:
            radiis = [self.parameters['radius_mean']] * self.total_population_num
            max_radius = self.parameters['radius_mean']    
        
        # calculate grid cells for placement of pedestrians
        grid_cell_size = max_radius*2+0.05 #multiple 2 because there needs diameter      
        grid = self._generate_placement_area(self.parameters, start_areas, grid_cell_size)
        if self.total_population_num > len(grid):
            print ("Warning: asked to create %d pedestrians, but only room for %d" % (self.total_population_num, len(grid)))
            return
        
        """select random placement and radii for each pedestrian type """
        """ create young pedestrians and then add into final population """ 
        
        """ pedestrian type = 0:young, 1:adult, 2:elderly """
        """ pedestrian type = 3: average   """
        """ pedestrian type = 4: average_cut off _lv3"""
        """ pedestrian type = 5: average_cut off _lv1"""
        """ pedestrian type = 6: uniform_cut off _lv3"""
        """ pedestrian type = 7: uniform_cut off _lv1"""
 
        
        cells = random.sample(grid, min(self.total_population_num,len(grid)))
        
        """"copy the same cells and radiis values for other prototypes """
        self.cells_average_pedestrians = list(cells)
        self.cells_average_cutoff_lv3_pedestrians = list(cells)
        self.cells_average_cutoff_lv1_pedestrians = list(cells)
        self.cells_uniform_cutoff_lv3_pedestrians = list(cells)
        self.cells_uniform_cutoff_lv1_pedestrians = list(cells)                                                 
                                                         
        self.radii_average_pedestrians=[]
        for radii in radiis:
            self.radii_average_pedestrians.append(radii)
        
        self.radii_average_cutoff_lv3_pedestrians=[]
        for radii in radiis:
            self.radii_average_cutoff_lv3_pedestrians.append(radii)
            
        self.radii_average_cutoff_lv1_pedestrians=[]
        for radii in radiis:
            self.radii_average_cutoff_lv1_pedestrians.append(radii)
            
        self.radii_uniform_cutoff_lv3_pedestrians=[]
        for radii in radiis:
            self.radii_uniform_cutoff_lv3_pedestrians.append(radii)
               
        self.radii_uniform_cutoff_lv1_pedestrians=[]
        for radii in radiis:
            self.radii_uniform_cutoff_lv1_pedestrians.append(radii)
        
        """ select random values of cells and radiis for each pedestrian type"""
        """ check pedestrian_Id """
        self.different_generated_pedestrian_index = 0
        self.average_generated_pedestrian_index = 0
        self.average_generated_cutoff_lv3_index = 0
        self.average_generated_cutoff_lv1_index = 0  
        self.uniform_generated_cutoff_lv3_index = 0
        self.uniform_generated_cutoff_lv1_index = 0
        
        if self.young_num > 0:
            self.cells_for_young = random.sample(cells, self.young_num)
            self.radii_for_young = random.sample(radiis, self.young_num)
           
            young_pedestrians= self._create_pedestrian_by_distribution(0, self.cells_for_young, self.radii_for_young, grid_cell_size,log_generation)
            self.different_generated_pedestrians.extend(young_pedestrians)
            
            cells = constants.remove_subset(cells,self.cells_for_young)
            radiis = constants.remove_subset(radiis,self.radii_for_young)
            
        if  self.adults_num >0:     
            self.cells_for_adult = random.sample(cells, self.adults_num)
            self.radii_for_adult = random.sample(radiis,self.adults_num)
            
            adult_pedestrians = self._create_pedestrian_by_distribution(1, self.cells_for_adult, self.radii_for_adult, grid_cell_size,log_generation)
            self.different_generated_pedestrians.extend(adult_pedestrians)
            
            cells = constants.remove_subset(cells,self.cells_for_adult)
            radiis = constants.remove_subset(radiis,self.radii_for_adult)
        
        if self.elderly_num>0:
            self.cells_for_elderly = cells
            self.radii_for_elderly= radiis
            elderly_pedestrians = self._create_pedestrian_by_distribution(2, self.cells_for_elderly, self.radii_for_elderly, grid_cell_size,log_generation)
            self.different_generated_pedestrians.extend(elderly_pedestrians)
        
        """ generate average population """
        self.average_generated_pedestrians = self._create_pedestrian_by_distribution(3, self.cells_average_pedestrians, self.radii_average_pedestrians, grid_cell_size,log_generation)
         
        """ generate average population cutoff_lv3"""
        self.average_cutoff_lv3_generated_pedestrians = self._create_pedestrian_by_distribution(4, self.cells_average_cutoff_lv3_pedestrians, self.radii_average_cutoff_lv3_pedestrians, grid_cell_size,log_generation)
         
        """ generate average population cutoff_lv1"""
        self.average_cutoff_lv1_generated_pedestrians = self._create_pedestrian_by_distribution(5, self.cells_average_cutoff_lv1_pedestrians, self.radii_average_cutoff_lv1_pedestrians, grid_cell_size,log_generation)
       
        """ generate uniform population cutoff_lv3"""
        self.uniform_cutoff_lv3_generated_pedestrians = self._create_pedestrian_by_distribution(6, self.cells_uniform_cutoff_lv3_pedestrians, self.radii_uniform_cutoff_lv3_pedestrians, grid_cell_size,log_generation)
       
        """ generate uniform population cutoff_lv3"""
        self.uniform_cutoff_lv1_generated_pedestrians = self._create_pedestrian_by_distribution(7, self.cells_uniform_cutoff_lv1_pedestrians, self.radii_uniform_cutoff_lv1_pedestrians, grid_cell_size,log_generation)
       

    def _create_pedestrian_by_distribution(self, pes_type, designated_cells, radiis, grid_cell_size,log_generation):

        pedestrians_in_same_type =[]
        velocities =[]
        relaxation_times =[]
        interaction_strengths = []
        interaction_ranges = []
        
        seedId = datetime.now().microsecond                      
        
        if pes_type == 0: # young people
            velocities = self.children_dist._get_children_desired_velocities_distribution()
            relaxation_times = self.children_dist._get_children_relaxation_times_distribution()
            interaction_strengths =  self.children_dist._get_children_interaction_strengths_distribution()
            interaction_ranges = self.children_dist._get_children_interaction_ranges_distribution()
            if log_generation:
                random.seed(seedId)
                self.children_seed = seedId

        elif pes_type ==1: # adult people
            velocities = self.adults_dist._get_adults_desired_velocities_distribution()
            relaxation_times = self.adults_dist._get_adults_relaxation_times_distribution()
            interaction_strengths =  self.adults_dist._get_adults_interaction_strengths_distribution()
            interaction_ranges = self.adults_dist._get_adults_interaction_ranges_distribution() 
            if log_generation:
                random.seed(seedId)
                self.adult_seed = seedId
                     
        elif pes_type == 2: # elderly people = 2
            velocities = self.elderly_dist._get_elderly_desired_velocities_distribution()
            relaxation_times = self.elderly_dist._get_elderly_relaxation_times_distribution()
            interaction_strengths =  self.elderly_dist._get_elderly_interaction_strengths_distribution()
            interaction_ranges = self.elderly_dist._get_elderly_interaction_ranges_distribution()
            if log_generation:
                random.seed(seedId)
                self.elderly_seed = seedId
                 
        elif pes_type==3: # average people =3 
            velocities = self.average_dist.get_average_desired_velocities()
            relaxation_times = self.average_dist.get_average_relaxation_times()
            interaction_strengths =  self.average_dist.get_average_interaction_strengths()
            interaction_ranges = self.average_dist.get_average_interaction_ranges()
            if log_generation:
                random.seed(seedId)
                self.average_seed = seedId
        
        elif pes_type==4: # average cutoff level3 
            velocities = self.average_dist.get_average_cutoff_lv_3_desired_velocities()
            relaxation_times = self.average_dist.get_average_cutoff_lv_3_relaxation_times()
            interaction_strengths =  self.average_dist.get_average_cutoff_lv_3_interaction_strengths()
            interaction_ranges = self.average_dist.get_average_cutoff_lv_3_interaction_ranges()
            if log_generation:
                random.seed(seedId)
                self.average_cutoff_lv3_seed = seedId
                
        elif pes_type==5: # average cutoff level1 
            velocities = self.average_dist.get_average_cutoff_lv_1_desired_velocities()
            relaxation_times = self.average_dist.get_average_cutoff_lv_1_relaxation_times()
            interaction_strengths =  self.average_dist.get_average_cutoff_lv_1_interaction_strengths()
            interaction_ranges = self.average_dist.get_average_cutoff_lv_1_interaction_ranges()
            if log_generation:
                random.seed(seedId)
                self.average_cutoff_lv1_seed = seedId
        
        elif pes_type==6: # uniform cutoff level3 
            velocities = self.average_dist.get_uniform_cutoff_lv_3_desired_velocities()
            relaxation_times = self.average_dist.get_uniform_cutoff_lv_3_relaxation_times()
            interaction_strengths =  self.average_dist.get_uniform_cutoff_lv_3_interaction_strengths()
            interaction_ranges = self.average_dist.get_uniform_cutoff_lv_3_interaction_ranges()
            if log_generation:
                random.seed(seedId)
                self.uniform_cutoff_lv3_seed = seedId
                
        elif pes_type==7: # uniform cutoff level1 
            velocities = self.average_dist.get_uniform_cutoff_lv_1_desired_velocities()
            relaxation_times = self.average_dist.get_uniform_cutoff_lv_1_relaxation_times()
            interaction_strengths =  self.average_dist.get_uniform_cutoff_lv_1_interaction_strengths()
            interaction_ranges = self.average_dist.get_uniform_cutoff_lv_1_interaction_ranges()
            if log_generation:
                random.seed(seedId)
                self.uniform_cutoff_lv1_seed = seedId
                        
                                                 
        for i in range(len(designated_cells)):
            radius = radiis[i]
            velocity = velocities[i]
            cell = designated_cells[i]
            free_space_x = grid_cell_size - radius*2
            free_space_y = grid_cell_size - radius*2
            x_coord = random.random() * free_space_x + cell[0] + radius
            y_coord = random.random() * free_space_y + cell[1] + radius
            position = (x_coord, y_coord)
            target = cell[2]
            
            pedestrian_id = 0
            
            if pes_type ==0 or pes_type == 1 or pes_type == 2:
                self.different_generated_pedestrian_index+=1
                pedestrian_id = self.different_generated_pedestrian_index
            
            elif pes_type == 3:
                self.average_generated_pedestrian_index +=1
                pedestrian_id = self.average_generated_pedestrian_index
                               
            elif pes_type == 4:
                self.average_generated_cutoff_lv3_index +=1
                pedestrian_id = self.average_generated_cutoff_lv3_index
                
            elif pes_type == 5:
                self.average_generated_cutoff_lv1_index +=1
                pedestrian_id = self.average_generated_cutoff_lv1_index    
            
            elif pes_type == 6:
                self.uniform_generated_cutoff_lv3_index +=1
                pedestrian_id = self.uniform_generated_cutoff_lv3_index
            
            elif pes_type == 7:
                self.uniform_generated_cutoff_lv1_index +=1
                pedestrian_id = self.uniform_generated_cutoff_lv1_index    
                            
            pedestrians_in_same_type.append(dict(
                p_type = pes_type,
                pedestrian_id = pedestrian_id,
                
                position = position,
                radius = radiis[i],
                initial_position = position,
                
                acceleration = (0.0, 0.0),
                initial_desired_velocity = velocity,
                velocity = (0.0, 0.0),
                time = 0.0,
                relax_time = relaxation_times[i],
                max_velocity = velocity * self.parameters['max_velocity_factor'],
                target = target,
                 
                force_unit = interaction_strengths[i],
                interaction_range = interaction_ranges[i],
                interaction_lamda = self.parameters['lambda'],
                
                desired_force_tracking = (0.0,0.0),
                interaction_force_tracking = (0.0,0.0),
                obstacle_force_tracking = (0.0,0.0)))
                   
        
        return pedestrians_in_same_type
    
    def _get_different_pedestrians_population(self):
        return self.different_generated_pedestrians
    
    def _get_averaged_pedestrians_population(self): 
        return self.average_generated_pedestrians
    
    def _get_a_cutoff_lv3_pedestrians_population(self):
        return self.average_cutoff_lv3_generated_pedestrians
    
    def _get_a_cutoff_lv1_pedestrians_population(self):
        return self.average_cutoff_lv1_generated_pedestrians
    
    def _get_u_cutoff_lv3_pedestrians_population(self):
        return self.uniform_cutoff_lv3_generated_pedestrians
    
    def _get_u_cutoff_lv1_pedestrians_population(self):
        return self.uniform_cutoff_lv1_generated_pedestrians
    
    def _generate_placement_area(self,parameters, start_areas,cell_size):
        grid = list()
        for i in range(len(start_areas)):
            (x1,y1,x2,y2) = start_areas[i]
            t = parameters['targets'][i] #define the target so that pedestrian will try to reach this destination
            x_range = x2-x1
            y_range = y2-y1
            x_offset = (x_range % cell_size)/2
            y_offset = (y_range % cell_size)/2
            cells_x = int(math.floor(x_range / cell_size))
            cells_y = int(math.floor(y_range / cell_size))
            
            for i in range(cells_x):
                for j in range(cells_y):
                    grid.append((i * cell_size + x_offset + x1, 
                        j * cell_size + y_offset + y1, t))
        return grid
    
    def _log_generation(self, log_dir):
        population_log =   PopulationLog(self.young_num,
                                         self.adults_num,
                                         self.elderly_num,
                                         
                                         self.children_dist._to_JSON(),
                                         self.radii_for_young,
                                         self.cells_for_young,
                                         self.children_seed,
                                         
                                         self.adults_dist._to_JSON(),
                                         self.radii_for_adult,
                                         self.cells_for_adult,
                                         self.adult_seed,
                                         
                                         self.elderly_dist._to_JSON(),
                                         self.radii_for_elderly,
                                         self.cells_for_elderly,
                                         self.elderly_seed,
                                         
                                         self.average_dist._to_JSON(),
                                         self.radii_average_pedestrians,
                                         self.cells_average_pedestrians,
                                         self.average_seed,
                                         
                                         self.radii_average_cutoff_lv3_pedestrians,
                                         self.cells_average_cutoff_lv3_pedestrians,                                       
                                         self.average_cutoff_lv3_seed,
                                         
                                         self.radii_average_cutoff_lv1_pedestrians,
                                         self.cells_average_cutoff_lv1_pedestrians,                                         
                                         self.average_cutoff_lv1_seed,
                                         
                                         self.radii_uniform_cutoff_lv3_pedestrians,
                                         self.cells_uniform_cutoff_lv3_pedestrians,                                         
                                         self.uniform_cutoff_lv3_seed,
                                         
                                         self.radii_uniform_cutoff_lv1_pedestrians,
                                         self.cells_uniform_cutoff_lv1_pedestrians,    
                                         self.uniform_cutoff_lv1_seed
                                         )
        
        log_file = open( "%s.log" % log_dir, "w")

        json_obj = json.dumps(population_log, cls=PopulationLog_Encoder)
        log_file.write(json_obj)
        log_file.close()