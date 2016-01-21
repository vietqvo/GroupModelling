'''
Created on 13 Feb 2015

@author: quangv
'''
import pygame
from pygame import gfxdraw
from src import constants 

BG_WHITE_COLOUR = (255,255,255)
DRAW__DARK_COLOUR = (0,0,0)
TARGET_PINK__COLOUR = (255,0,127)

START_AREA_COLOUR = (148,154,70)
TRACKING_AREA_COLOUR = (153,153,0)

DESIRED_FORCE__COLOUR = (76,153,0) #green
INTERACTION_FORCE__COLOUR = (255,0,0) #red
OBSTACLE_FORCE__COLOUR = (255,128,0) #brown
TRAIL_COLOUR = (153,0,0)
COLOURS = [
        (102,204,0), # green color
        (255,0,0), # red color
        (0,0,255), # blue color
        (0,0,0), #black color for average prototype
        (153,0,76), #yellow color for average cutoff level3 pedestrian
        (255,128,0),#brown color for average cutoff level1 pedestrian
        (204,102,0),#orange color for uniform cutoff level3 pedestrian
        (0,204,204)# light blue color for uniform cutoff level1 pedestrian
        
        ]
class Canvas:
    """This class is to manage canvas and its object """
    def __init__(self, width, height, factor, image_prefix, video_prefix, simulationId):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption("Group behavior simulation")
        self.pixel_factor = factor
        
        self.image_prefix = image_prefix
        self.video_prefix = video_prefix
        self.simulationId = simulationId
        
        self.target_colours = dict()
        self.font = pygame.font.Font(None, 18)
        self.clock = pygame.time.Clock()
    
        self.pedestrian_pos_track = [-100.0,-100.0]
        
    def quit(self):
        pygame.display.quit()
    
    def clear_screen(self):
        self.screen.fill(BG_WHITE_COLOUR)
        
    def tick(self,framerate):
        self.clock.tick(framerate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True  
    
    def update(self):
        pygame.display.flip()
        
    def create_image(self, frames):
        ext = "png"
        pygame.image.save(self.screen, "%s-%s.%s" % (self.image_prefix, self.simulationId, ext))
        
    def _draw_circle(self, x, y, radii, color):       
        gfxdraw.aacircle(self.screen, x, y, radii, color)    
    
    def _draw_filled_circle(self,x,y,radii,color):
        gfxdraw.filled_circle(self.screen, x, y, radii, color)    
                   
    def _draw_line(self, x1, y1, x2, y2, c):
        gfxdraw.line(self.screen, x1, y1, x2, y2, c)

    def draw_wall(self, w):
        (x1,y1) = self.screen_coords(w[0], w[1])
        (x2,y2) = self.screen_coords(w[2], w[3])
        self._draw_line(x1, y1, x2, y2, DRAW__DARK_COLOUR)

    def _get_colour(self, t):
        if not t in self.target_colours:
            self.target_colours[t] = COLOURS[len(self.target_colours)]
        return self.target_colours[t]
    
    def draw_start_area(self, t):
        (x1,y1) = self.screen_coords(t[0], t[1])
        (x2,y2) = self.screen_coords(t[2], t[3])
        pygame.draw.rect(self.screen, DRAW__DARK_COLOUR, (x1, y1, x2-x1, y2-y1),1)
      
           
    def draw_group_center(self,group_center_x,group_center_y):
        group_center_x = constants.myround(group_center_x,4)
        group_center_y = constants.myround(group_center_y,4)
        (group_center_x,group_center_y) = self.screen_coords(group_center_x,group_center_y)
        pygame.draw.circle(self.screen, INTERACTION_FORCE__COLOUR, (group_center_x,group_center_y), self.screen_radius(0.2), 0)
        
    
    def draw_pedestrian(self, x, y, r, t,checked=-1, 
                        desired_force_vector=(0.0,0.0),
                        interaction_force_vector=(0.0,0.0),
                        tracked_obstacle_force_vector =(0.0,0.0),
                        tracked_initial_posistion=(0.0,0.0)): 
       
        (x,y) = self.screen_coords(x,y)
        self._draw_circle(x, y, self.screen_radius(r), DRAW__DARK_COLOUR)
     
                
    def draw_target(self, x, y):
        (x,y) = self.screen_coords(x,y)
        if x > self.width or x < -self.width or y > self.height or y < -self.height:
            return
        pygame.draw.circle(self.screen, TARGET_PINK__COLOUR, (x,y), self.screen_radius(0.2), 0)

    def draw_text(self, t, draw_fps=True):
        if draw_fps:
            text = "%s - %d fps" % (t, self.clock.get_fps())
        else:
            text = t
        texture = self.font.render(text, 
                True, DRAW__DARK_COLOUR, BG_WHITE_COLOUR)
        self.screen.blit(texture, texture.get_rect())
    
    def screen_coords(self, x, y):
       
        x *= self.pixel_factor
        y *= self.pixel_factor

        shift_w = self.width/2
        shift_h = self.height/2
    
        x += shift_w
        y += shift_h
        
        return (int(x),int(y))
    
    def screen_radius(self, r):
        return int(r*self.pixel_factor)
            