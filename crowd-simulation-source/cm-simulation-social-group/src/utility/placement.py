'''
Created on 28 Sep 2015

@author: quangv
'''
from src import constants
import math, random

class PlacementGenerator(object):
    
    def __init__(self, parameters, outgroup_num, children_group_num, adults_group_num, elderly_group_num):
        self.parameters = parameters
     
        self._reset_placements()
        
        self.total_population_num = children_group_num + adults_group_num + elderly_group_num + outgroup_num
        
        self.outgroup_num = outgroup_num
        self.children_group_num = children_group_num
        self.adults_group_num = adults_group_num
        self.elderly_group_num = elderly_group_num
         
    def _reset_placements(self):
        
        self.max_radius = 0
       
        self.placements_for_young = []
        self.placements_for_adult = []
        self.placements_for_elderly = []
        self.placements_for_out_group_peds = []
               
    def _generate_placements(self, start_areas,
                             max_radius, 
                             radii_children, 
                             raddi_adults,
                             radii_elders,
                             radii_outgroup_peds):
        
        # calculate grid cells for placement of pedestrians
        grid_cell_size = max_radius*2+0.05 #multiple 2 because there needs diameter      
        grid = self._generate_placement_area(self.parameters, start_areas, grid_cell_size)
        if self.total_population_num > len(grid):
            print ("Warning: asked to create %d pedestrians, but only room for %d" % (self.total_population_num, len(grid)))
            return
        
        """select random placement and radii for each pedestrian type """
        """ create young pedestrians and then add into final population """ 
        
        """ pedestrian type = 0:young group members, 1:adult group members, 2:elderly group members"""
        """ pedestrian type = 3: out-group pedestrians   """
      
        cells = random.sample(grid, min(self.total_population_num,len(grid)))        
     
        if self.children_group_num > 0:
            cells_for_young = random.sample(cells, self.children_group_num)
            self.placements_for_young= self._create_placement_for_pedestrian_type(0, cells_for_young, radii_children, grid_cell_size) 
            cells = constants.remove_subset(cells,cells_for_young)
            
        if  self.adults_group_num >0:     
            cells_for_adult = random.sample(cells, self.adults_group_num)
            self.placements_for_adult = self._create_placement_for_pedestrian_type(1, cells_for_adult, raddi_adults, grid_cell_size)
            cells = constants.remove_subset(cells,cells_for_adult)
      
        if self.elderly_group_num>0:
            cells_for_elderly = random.sample(cells, self.elderly_group_num) 
            self.placements_for_elderly = self._create_placement_for_pedestrian_type(2, cells_for_elderly, radii_elders, grid_cell_size)
            cells = constants.remove_subset(cells,self.cells_for_elderly)
    
        if self.outgroup_num > 0:
            cells_for_out_group_peds = cells
            self.placements_for_out_group_peds = self._create_placement_for_pedestrian_type(3, cells_for_out_group_peds, radii_outgroup_peds, grid_cell_size)
     
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
            target = cell[2]
            
            pedestrians_in_same_type.append(dict(
                position = position,
                target = target))
                    
        return pedestrians_in_same_type
     
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
        
    def _get_max_radius(self):
        return self.max_radius
    
    def _set_max_radius(self,radius):
        self.max_radius = radius
        
    def _get_placements_for_young(self):
        return self.placements_for_young      
    
    def _set_placements_for_young(self,placements):
        self.placements_for_young = placements   
    
    def _get_placements_for_adult(self):
        return self.placements_for_adult      
    
    def _set_placements_for_adult(self, placements):
        self.placements_for_adult = placements   
        
    def _get_placements_for_elderly(self):
        return self.placements_for_elderly      
    
    def _set_placements_for_elderly(self, placements):
        self.placements_for_elderly =   placements  
        
    def _get_placements_for_out_group_peds(self):
        return self.placements_for_out_group_peds
    
    def _set_placements_for_out_group_peds(self,placements):
        self.placements_for_out_group_peds = placements
    
    def _get_total_population(self):
        return self.total_population_num
    
    def _set_total_population(self,total_num):
        self.total_population_num = total_num