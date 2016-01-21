'''
Created on 13 Feb 2015

@author: quangv
'''
import constants
import numpy, math, random
from datetime import datetime
from quantification import QuantitativePlots

class PopulationGenerator:
    def __init__(self, parameters= {}):
        self.parameters = parameters
        
        self.pedestrians =[]
        self.average_generated_pedestrians = []
    
    def _create_pedestrian_by_distribution(self, pes_type, num, designated_cells, radiis, grid_cell_size):

        pedestrians_in_same_type =[]
        velocities =[]
        relaxation_times =[]
        force_strengths = []
        interaction_ranges = []
        
        if pes_type == 0: # young people
            if self.parameters['young_velocity_deviation'] > 0.0:
                while True:
                    velocities = numpy.random.normal(self.parameters['young_velocity_mean'], self.parameters['young_velocity_deviation'], num)
                    if self._check_numpy_gaussian_sampling(velocities,self.parameters['young_velocity_mean']) == 1:
                        break
            else:
                velocities = [self.parameters['young_velocity_mean']] * num
            
            if self.parameters['young_relaxation_deviation'] > 0.0:
                while True:   
                    relaxation_times = numpy.random.normal(self.parameters['young_relaxation_mean'], self.parameters['young_relaxation_deviation'], num)
                    if self._check_numpy_gaussian_sampling(relaxation_times,self.parameters['young_relaxation_mean']) == 1:
                        break
            else:
                relaxation_times = [self.parameters['young_relaxation_mean']] * num
            
            if self.parameters['young_force_deviation'] > 0.0: 
                while True:      
                    force_strengths =  numpy.random.normal(self.parameters['young_force_unit'], self.parameters['young_force_deviation'], num)
                    if self._check_numpy_gaussian_sampling(force_strengths,self.parameters['young_force_unit']) == 1:
                        break
            else:
                force_strengths = [self.parameters['young_force_unit']] * num
            
            if self.parameters['young_range_deviation'] > 0.0:
                while True:        
                    interaction_ranges = numpy.random.normal(self.parameters['young_force_range'], self.parameters['young_range_deviation'], num)
                    if self._check_numpy_gaussian_sampling(interaction_ranges,self.parameters['young_force_range']) == 1:
                        break
            else:
                interaction_ranges = [self.parameters['young_force_range']] * num
                 
        elif pes_type ==1: # adult people
            if self.parameters['adult_velocity_deviation'] > 0.0:
                while True:
                    velocities = numpy.random.normal(self.parameters['adult_velocity_mean'], self.parameters['adult_velocity_deviation'], num)
                    if self._check_numpy_gaussian_sampling(velocities,self.parameters['adult_velocity_mean']) == 1:
                        break   
            else:
                velocities = [self.parameters['adult_velocity_mean']] * num
            
            if self.parameters['adult_relaxation_deviation'] > 0.0:
                while True:  
                    relaxation_times = numpy.random.normal(self.parameters['adult_relaxation_mean'], self.parameters['adult_relaxation_deviation'], num)
                    if self._check_numpy_gaussian_sampling(relaxation_times,self.parameters['adult_relaxation_mean']) == 1:
                        break 
            else:
                relaxation_times = [self.parameters['adult_relaxation_mean']] * num
            
            if self.parameters['adult_force_deviation'] > 0.0:
                while True:        
                    force_strengths =  numpy.random.normal(self.parameters['adult_force_unit'], self.parameters['adult_force_deviation'], num)
                    if self._check_numpy_gaussian_sampling(force_strengths,self.parameters['adult_force_unit']) == 1:
                        break 
            else:
                force_strengths = [self.parameters['adult_force_unit']] * num
            
            if self.parameters['adult_range_deviation'] > 0.0:
                while True:
                    interaction_ranges = numpy.random.normal(self.parameters['adult_force_range'], self.parameters['adult_range_deviation'], num)
                    if self._check_numpy_gaussian_sampling(interaction_ranges,self.parameters['adult_force_range']) == 1:
                        break 
            else:
                interaction_ranges =  [self.parameters['adult_force_range']] * num
        
        else: # elderly people = 2
            if self.parameters['elderly_velocity_deviation'] > 0.0:
                while True:
                    velocities = numpy.random.normal(self.parameters['elderly_velocity_mean'], self.parameters['elderly_velocity_deviation'], num)
                    if self._check_numpy_gaussian_sampling(velocities,self.parameters['elderly_velocity_mean']) == 1:
                        break 
            else:
                velocities = [self.parameters['elderly_velocity_mean']] * num
            
            if self.parameters['elderly_relaxation_deviation'] > 0.0:    
                while True:
                    relaxation_times = numpy.random.normal(self.parameters['elderly_relaxation_mean'], self.parameters['elderly_relaxation_deviation'], num)
                    if self._check_numpy_gaussian_sampling(relaxation_times,self.parameters['elderly_relaxation_mean']) == 1:
                        break
            else:
                relaxation_times = [self.parameters['elderly_relaxation_mean']] * num
            
            if self.parameters['elderly_force_deviation'] > 0.0:
                while True:    
                    force_strengths =  numpy.random.normal(self.parameters['elderly_force_unit'], self.parameters['elderly_force_deviation'], num)
                    if self._check_numpy_gaussian_sampling(force_strengths,self.parameters['elderly_force_unit']) == 1:
                        break
            else:
                force_strengths = [self.parameters['elderly_force_unit']] * num
            
            if self.parameters['elderly_range_deviation'] > 0.0:
                while True:
                    interaction_ranges = numpy.random.normal(self.parameters['elderly_force_range'], self.parameters['elderly_range_deviation'], num)
                    if self._check_numpy_gaussian_sampling(interaction_ranges,self.parameters['elderly_force_range']) == 1:
                        break
            else:
                interaction_ranges = [self.parameters['elderly_force_range']] * num
           
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
            
            pedestrians_in_same_type.append(dict(
                p_type = pes_type,
                position = position,
                radius = radiis[i],
    
                
                acceleration = (0.0, 0.0),
                initial_desired_velocity = velocity,
                velocity = (0.0, 0.0),
                time = 0.0,
                relax_time = relaxation_times[i],
                target = target,
                 
                interaction_constant = force_strengths[i],
                interaction_distance = interaction_ranges[i]))
    
        return pedestrians_in_same_type
    
   
    def _get_pedestrian_type_population(self):
        return self.pedestrians
    
    def _get_averaged_pedestrians(self):
        return self.average_generated_pedestrians
 
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
    
    def _generate_general_pedestrians(self, pes_type, pedestrians, radiis, cells_average_pedestrians,grid_cell_size):
        
        general_pedestrians = []
        total_population = len(pedestrians)
        if total_population==0:
            return general_pedestrians
        
        # extract velocity information from pedestrians list
        pedestrians_velocities = [(pedestrian['initial_desired_velocity']) for pedestrian in pedestrians]
        while True:
            velocities = numpy.random.normal(numpy.mean(pedestrians_velocities), numpy.std(pedestrians_velocities), total_population)
            if self._check_numpy_gaussian_sampling(velocities,numpy.mean(pedestrians_velocities)) == 1:
                break
            
        pedestrians_acceleration_time = [(pedestrian['relax_time']) for pedestrian in pedestrians]
        while True:
            acceleration_times = numpy.random.normal(numpy.mean(pedestrians_acceleration_time), numpy.std(pedestrians_acceleration_time), total_population)
            if self._check_numpy_gaussian_sampling(acceleration_times,numpy.mean(pedestrians_acceleration_time)) == 1:
                break
            
        pedestrians_interaction_strength = [(pedestrian['interaction_constant']) for pedestrian in pedestrians]
        while True:
            interaction_strengths = numpy.random.normal(numpy.mean(pedestrians_interaction_strength), numpy.std(pedestrians_interaction_strength), total_population)
            if self._check_numpy_gaussian_sampling(interaction_strengths,numpy.mean(pedestrians_interaction_strength)) == 1:
                break
        
        pedestrians_interaction_distance = [(pedestrian['interaction_distance']) for pedestrian in pedestrians]
        while True:
            interaction_distances = numpy.random.normal(numpy.mean(pedestrians_interaction_distance), numpy.std(pedestrians_interaction_distance), total_population)
            if self._check_numpy_gaussian_sampling(interaction_distances,numpy.mean(pedestrians_interaction_distance)) == 1:
                break
            
        for i in range(len(cells_average_pedestrians)):
            radius = radiis[i]
            velocity = velocities[i]
            cell = cells_average_pedestrians[i]
            free_space_x = grid_cell_size - radius*2
            free_space_y = grid_cell_size - radius*2
            x_coord = random.random() * free_space_x + cell[0] + radius
            y_coord = random.random() * free_space_y + cell[1] + radius
            position = (x_coord, y_coord)
            target = cell[2]
            
            general_pedestrians.append(dict(
                p_type = pes_type,
                position = position,
                radius = radiis[i],
    
                
                acceleration = (0.0, 0.0),
                initial_desired_velocity = velocity,
                velocity = (0.0, 0.0),
                time = 0.0,
                relax_time = acceleration_times[i],
                target = target,
                 
                interaction_constant = interaction_strengths[i],
                interaction_distance = interaction_distances[i]))
        
        """shuffle pedestrian list """
        random.shuffle(general_pedestrians)
        return general_pedestrians
            
    def _generate_population(self, start_areas, young_num, adult_num, elderly_num, quantification_plots=False):
   
        self.pedestrians = []
        self.average_generated_pedestrians = []
         
        young_pedestrians =[]
        adult_pedestrians =[]
        elderly_pedestrians =[]
        
        total_population = young_num + adult_num + elderly_num
        
        if total_population==0:
            return
        
        # generate radii for all population
        if self.parameters['radius_deviation'] > 0.0:
            while True:
                radiis = numpy.random.normal(self.parameters['radius_mean'],self.parameters['radius_deviation'], total_population)
                if self._check_numpy_gaussian_sampling(radiis,self.parameters['radius_mean']) == 1:
                    break
            radiis = constants.myround(radiis,4)# we only get 4 decimal points
            radiis = radiis.tolist()
            max_radius = max(radiis)
        else:
            radiis = [self.parameters['radius_mean']] * total_population
            max_radius = self.parameters['radius_mean']    
        
        # calculate grid cells for placement of pedestrians
        grid_cell_size = max_radius*2+0.05 #multiple 2 because there needs diameter      
        grid = self._generate_placement_area(self.parameters, start_areas, grid_cell_size)
        if total_population > len(grid):
            print ("Warning: asked to create %d pedestrians, but only room for %d" % (total_population, len(grid)))
            return
        
        """select random placement and radii for each pedestrian type """
        """ create young pedestrians and then add into final population """ 
        """ pedestrian type = 0:young, 1:adult, 2:elderly """
        """ pedestrian type = 3: average   """
        cells = random.sample(grid, min(total_population,len(grid)))
        
        cells_average_pedestrians = list(cells)
        radii_average_pedestrians=[]
        for radii in radiis:
            radii_average_pedestrians.append(radii)
        
        if young_num > 0:
            cells_for_young = random.sample(cells, young_num)
            radii_for_young = random.sample(radiis, young_num)
            young_pedestrians= self._create_pedestrian_by_distribution(0, young_num, cells_for_young, radii_for_young,grid_cell_size)
            self.pedestrians.extend(young_pedestrians)
    
            
            cells = constants.remove_subset(cells,cells_for_young)
            radiis = constants.remove_subset(radiis,radii_for_young)
            
        if  adult_num >0:     
            cells_for_adult = random.sample(cells, adult_num)
            radii_for_adult = random.sample(radiis,adult_num)
            adult_pedestrians = self._create_pedestrian_by_distribution(1, adult_num, cells_for_adult, radii_for_adult,grid_cell_size)
            self.pedestrians.extend(adult_pedestrians)
      
            cells = constants.remove_subset(cells,cells_for_adult)
            radiis = constants.remove_subset(radiis,radii_for_adult)
        
        if elderly_num>0: 
            elderly_pedestrians = self._create_pedestrian_by_distribution(2, elderly_num, cells, radiis,grid_cell_size)
            self.pedestrians.extend(elderly_pedestrians)
        
        ##### generate average population based on above three pedestrian types
        self.average_generated_pedestrians = self._generate_general_pedestrians(3, self.pedestrians, radii_average_pedestrians, cells_average_pedestrians,grid_cell_size)
        
        ##### quantitative plotting
        if quantification_plots ==True:
            quantitative_plot = QuantitativePlots(self.parameters,young_pedestrians,adult_pedestrians,elderly_pedestrians,self.average_generated_pedestrians,self.pedestrians)
            
            currentPlottingTime=datetime.now()
            currentPlottingTime = "%s" % (currentPlottingTime.microsecond);
            
            #plot parameter probability distribution
            quantitative_plot._create_pedestrian_type_distribution_plot("initial_desired_velocity", "Free Velocity", constants.quantification_plot_bin_num,currentPlottingTime)
            quantitative_plot._create_pedestrian_type_distribution_plot("relax_time", "Acceleration Time", constants.quantification_plot_bin_num,currentPlottingTime)
            quantitative_plot._create_pedestrian_type_distribution_plot("interaction_constant", "Interaction Strength", constants.quantification_plot_bin_num,currentPlottingTime)
            quantitative_plot._create_pedestrian_type_distribution_plot("interaction_distance", "Interaction Distance", constants.quantification_plot_bin_num,currentPlottingTime)
            
            #plot bell-curve fit distribution of each parameter
            quantitative_plot._create_bell_curve_distribution_plot("initial_desired_velocity", "Free Velocity", constants.quantification_plot_bin_num,currentPlottingTime)
            quantitative_plot._create_bell_curve_distribution_plot("relax_time", "Acceleration Time", constants.quantification_plot_bin_num,currentPlottingTime)
            quantitative_plot._create_bell_curve_distribution_plot("interaction_constant", "Interaction Strength", constants.quantification_plot_bin_num,currentPlottingTime)
            quantitative_plot._create_bell_curve_distribution_plot("interaction_distance", "Interaction Distance", constants.quantification_plot_bin_num,currentPlottingTime)
            
        """shuffle pedestrian list """
        random.shuffle(self.pedestrians)

    def _check_numpy_gaussian_sampling(self, array, value):
        mean = numpy.mean(array)
     
        if math.fabs(mean-value) < 0.01:
            return 1
        return 0