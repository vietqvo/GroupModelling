'''
Created on 13 Feb 2015

@author: quangv
'''
import math
import json
import random
from src import constants
from src.parameter_plots.distribution import DistributionPlot as distribution_plot
from src.pedestrian_types.average import Average as average_distribution
from src.pedestrian_types.population_log import PopulationLog
from src.pedestrian_types.population_log import PopulationLog_Encoder

class PopulationGenerator:
    
    def __init__(self, parameters, average_num, desire_velocity_array, force_array, quantification_plots, strTime):
        self.parameters = parameters
        
        self.average_generated_pedestrians = []
        self.total_population_num = average_num
        
        self.average_dist = average_distribution(self.total_population_num, desire_velocity_array, force_array,parameters)
          
        """ quantitative plotting """
        if quantification_plots ==True:
            quantitative_plot = distribution_plot(self.parameters)

            quantitative_plot._create_pedestrian_type_parameter_distribution_plot("Initial Desired Velocity", constants.quantification_plot_bin_num,
                                                                        self.average_dist._get_average_desired_velocities_distribution())
                 
            quantitative_plot._create_pedestrian_type_parameter_distribution_plot("Interaction Strength", constants.quantification_plot_bin_num,
                                                                        self.average_dist._get_average_interaction_strengths_distribution())
                       
            quantitative_plot._save_figure(strTime)
                  
    def _generate_population(self, start_areas,log_generation):
  
        self.average_generated_pedestrians = []
        
        grid_start_areas=[]
        self.cells_average_pedestrians = []
        self.cells_average_pedestrians.clear()
        
        for i in range(len(start_areas)):
            grid = list()
            (x1,x2) = start_areas[i]
            t = self.parameters['targets'][0]
            x_range = x2-x1
         
            x_offset = (x_range % constants.minimal_placement_distance)/2
            cells_x = int(math.floor(x_range / constants.minimal_placement_distance))
            for j in range(cells_x):
                grid.append((j * constants.minimal_placement_distance + x_offset + x1, t))
                
            grid_start_areas.append(grid)
               
        """select random placement and radii for each pedestrian type """   
        """ pedestrian type = average   """
        for i in range(len(grid_start_areas)):
            num_limit = int(self.total_population_num/len(grid_start_areas))
            cells_uni_side= random.sample(grid_start_areas[i], num_limit)
            for cell in cells_uni_side:
                self.cells_average_pedestrians.append(cell)
        
        self.average_generated_pedestrian_index = 0
        
        self.average_generated_pedestrians = self._create_pedestrian_by_distribution(self.cells_average_pedestrians, log_generation)
        
        return self.average_generated_pedestrians
    
    def _create_pedestrian_by_distribution(self, designated_cells,log_generation):

        pedestrians_in_same_type =[]
        print(designated_cells)
        
        velocities = self.average_dist._get_average_desired_velocities_distribution()
        interaction_strengths =  self.average_dist._get_average_interaction_strengths_distribution()
      
        for i in range(len(designated_cells)):
           
            velocity = velocities[i]
            cell = designated_cells[i]
 
            position = cell[0] 
            target = cell[1]
            
            self.average_generated_pedestrian_index +=1
            pedestrian_id = self.average_generated_pedestrian_index
                    
            pedestrians_in_same_type.append(dict(
                pedestrian_id = pedestrian_id,
                
                position = position,
                initial_position = position,
                initial_desired_velocity = velocity,
                acceleration = 0.0,
                velocity = 0.0,
                time = 0.0,
                target = target,
                force_unit = interaction_strengths[i],
                
                desired_force_tracking = 0.0,
                interaction_force_tracking = 0.0,
                distance_travelled = 0.0,
                is_not_moving=0.0))
                   
        
        return pedestrians_in_same_type
    
    def _get_averaged_pedestrians_population(self):
        return self.average_generated_pedestrians
    
    def _log_generation(self, log_dir):
        population_log =  PopulationLog(self.total_population_num, self.average_dist._to_JSON(), self.cells_average_pedestrians)
        log_file = open( "%s.log" % log_dir, "w")
        json_obj = json.dumps(population_log, cls=PopulationLog_Encoder)
        log_file.write(json_obj)
        log_file.close()