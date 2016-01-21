'''
Created on 28 Sep 2015

@author: quangv
'''
import math, random

class PlacementGenerator(object):
    
    def __init__(self, parameters, group_num):
        self.parameters = parameters
     
        self._reset_placements()
        
        self.total_population_num = group_num
             
    def _reset_placements(self):
        
        self.max_radius = 0
        self.placements_for_group = []

    def _generate_placements(self, start_areas,
                             max_radius, 
                             radii_group):
        
        # calculate grid cells for placement of pedestrians
        grid_cell_size = max_radius*2+0.05 #multiple 2 because there needs diameter      
        grid = self._generate_placement_area(self.parameters, start_areas, grid_cell_size)
        if self.total_population_num > len(grid):
            print ("Warning: asked to create %d pedestrians, but only room for %d" % (self.total_population_num, len(grid)))
            return
      
        cells = random.sample(grid, min(self.total_population_num,len(grid)))        
     
        if self.total_population_num > 0:
            cells_for_group = random.sample(cells, self.total_population_num)
            self.placements_for_group= self._create_placement_for_pedestrian_type(0, cells_for_group, radii_group, grid_cell_size) 
              
    def _create_placement_for_pedestrian_type(self,pes_type, designated_cells, radii, grid_cell_size):
        
        pedestrians_in_same_type =[]
        
        for i in range(len(designated_cells)):
            radius = radii[i]
            cell = designated_cells[i]
            free_space_x = grid_cell_size - radius*2
            free_space_y = grid_cell_size - radius*2
            x_coord = random.random() * free_space_x + cell[0] + radius
            y_coord = random.random() * free_space_y + cell[1] + radius
            position = (x_coord, y_coord)

            pedestrians_in_same_type.append(dict(
                position = position))
                    
        return pedestrians_in_same_type
     
    def _generate_placement_area(self,parameters, start_areas,cell_size):
        grid = list()
        for i in range(len(start_areas)):
            (x1,y1,x2,y2) = start_areas[i]
            x_range = x2-x1
            y_range = y2-y1
            x_offset = (x_range % cell_size)/2
            y_offset = (y_range % cell_size)/2
            cells_x = int(math.floor(x_range / cell_size))
            cells_y = int(math.floor(y_range / cell_size))
            
            for i in range(cells_x):
                for j in range(cells_y):
                    grid.append((i * cell_size + x_offset + x1, 
                        j * cell_size + y_offset + y1))
        return grid
        
    def _get_max_radius(self):
        return self.max_radius
    
    def _set_max_radius(self,radius):
        self.max_radius = radius
        
    def _get_placements_for_group(self):
        return self.placements_for_group      
    
    def _set_placements_for_group(self,placements):
        self.placements_for_group = placements   
    
    def _get_total_population(self):
        return self.total_population_num
    
    def _set_total_population(self,total_num):
        self.total_population_num = total_num