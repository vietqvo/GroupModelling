'''
Created on 28 Sep 2015

@author: quangv
'''
from src import constants
import numpy, random

class RadiiGenerator(object):
    
    def __init__(self, parameters, outgroup_num, children_group_num, adults_group_num, elderly_group_num):
        self.parameters = parameters
     
        self._reset_radii()
        
        self.total_population_num = children_group_num + adults_group_num + elderly_group_num + outgroup_num
        
        self.outgroup_num = outgroup_num
        self.children_group_num = children_group_num
        self.adults_group_num = adults_group_num
        self.elderly_group_num = elderly_group_num
        
    def _reset_radii(self):
      
        self.radii_for_young = []
        self.radii_for_adult = []
        self.radii_for_elderly=  []
        self.radii_for_out_group_peds = []
        
        self.max_radii = 0.0
    
    def _generate_radii(self):
        
        """ generate radii for all population """
        self.radii_for_young.clear()
        self.radii_for_adult.clear()
        self.radii_for_elderly.clear()
        self.radii_for_out_group_peds.clear()
        
        radiis = []
        if self.parameters['radius_deviation'] > 0.0:
            while len(radiis) < self.total_population_num:
                samples = numpy.random.normal(self.parameters['radius_mean'],self.parameters['radius_deviation'], self.total_population_num)           
                radiis.extend(constants._filter_samples_by_mean(samples, self.total_population_num-len(radiis)))          

            self.max_radii = max(radiis)
        else:
            self.pedestrian_radius = [self.parameters['radius_mean']] * self.total_population_num
            self.max_radius = self.parameters['radius_mean']    
        
        if self.children_group_num > 0:    
            self.radii_for_young = random.sample(radiis,self.children_group_num)
            radiis = constants.remove_subset(radiis,self.radii_for_young)
        
        if  self.adults_group_num >0:     
            self.radii_for_adult = random.sample(radiis,self.adults_group_num)
            radiis = constants.remove_subset(radiis,self.radii_for_adult)
              
        if self.elderly_group_num>0:
            self.radii_for_elderly=  random.sample(radiis,self.elderly_group_num)
            radiis = constants.remove_subset(radiis,self.radii_for_elderly)
         
        if self.outgroup_num > 0: 
            self.radii_for_out_group_peds = radiis
              
    def _get_radii_for_young(self):
        return self.radii_for_young
    
    def _set_radii_for_young(self,radii_young):
        self.radii_for_young = radii_young
         
    def _get_radii_for_adult(self):
        return self.radii_for_adult
    
    def _set_radii_for_adult(self, radii_adult):
        self.radii_for_adult = radii_adult
        
    def _get_radii_for_elderly(self):
        return self.radii_for_elderly
    
    def _set_radii_for_elderly(self,radii_elder):
        self.radii_for_elderly = radii_elder
        
    def _get_radii_for_outgroup(self):
        return self.radii_for_out_group_peds
    
    def _set_radii_for_outgroup(self,radii_outgroup):
        self.radii_for_out_group_peds = radii_outgroup
        
    def _get_max_radii(self):
        return self.max_radii   
    
    def _set_max_radii(self,max_radii):
        self.max_radii = max_radii 
    
    def _get_total_population(self):
        return self.total_population_num
    
    def _set_total_population(self,total_num):
        self.total_population_num = total_num