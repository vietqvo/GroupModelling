'''
Created on 13 Feb 2015

@author: quangv
'''
import pygame
from pygame import gfxdraw
from src import constants 
from math import hypot

BG_WHITE_COLOUR = (255,255,255)
DRAW__DARK_COLOUR = (0,0,0)
TARGET_PINK__COLOUR = (255,0,127)

START_AREA_COLOUR = (148,154,70)

DESIRED_FORCE__COLOUR = (76,153,0) #green
INTERACTION_FORCE__COLOUR = (255,0,0) #red
OBSTACLE_FORCE__COLOUR = (255,128,0) #brown
TRAIL_COLOUR = (153,0,0)
COLOURS = [
        (102,204,0), # green color
        (255,0,0), # red color
        (0,0,255), # blue color
        (0,0,0), #black color for average prototype
        (153,0,76) #yellow color for tracked pedestrian
        ]
class Canvas:
    """This class is to manage canvas and its object """
    def __init__(self, width, height, factor, image_prefix, video_prefix, simulationId):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption("Pedestrian Types_Social Force Model")
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.pedestrian_pos_track[0] == -100.0 and self.pedestrian_pos_track[1] == -100.0:
                    self.pedestrian_pos_track = pygame.mouse.get_pos()
                    self.pedestrian_pos_track = self.convert_pos_coords(self.pedestrian_pos_track[0],self.pedestrian_pos_track[1])
                    self.pedestrian_traj_track = list()
                    self.pedestrian_traj_track.clear()
                else:
                    print(">>>> Current version only supports one pedestrian tracked")
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
        pygame.draw.rect(self.screen, START_AREA_COLOUR, (x1, y1, x2-x1, y2-y1),1)
      
    def draw_pedestrian(self, x, y, r, t,checked=-1, 
                        desired_force_vector=(0.0,0.0),
                        interaction_force_vector=(0.0,0.0),
                        tracked_obstacle_force_vector =(0.0,0.0),
                        tracked_initial_posistion=(0.0,0.0)): 
   
        
        if checked==-1:
            (x,y) = self.screen_coords(x,y)
            colour = COLOURS[int(round(t))]
            self._draw_circle(x, y, self.screen_radius(r), colour)
        else:
            colour = COLOURS[4]  
          
            (x_desired,y_desired) = self.screen_coords(x+desired_force_vector[0],y+desired_force_vector[1])
            (x_interaction,y_interaction) = self.screen_coords(x+interaction_force_vector[0],y+interaction_force_vector[1])
            (x_obstacle,y_obstacle) = self.screen_coords(x+tracked_obstacle_force_vector[0],y+tracked_obstacle_force_vector[1])
            
            (x,y) = self.screen_coords(x,y)
            self._draw_filled_circle(x, y, self.screen_radius(r), colour)            
            
            #self._draw_line(x, y, x_desired, y_desired, DESIRED_FORCE__COLOUR)
            pygame.draw.aaline(self.screen, DESIRED_FORCE__COLOUR, [x, y], [x_desired, y_desired], True)
            
            #self._draw_line(x, y, x_interaction, y_interaction, INTERACTION_FORCE__COLOUR)
            pygame.draw.aaline(self.screen, INTERACTION_FORCE__COLOUR, [x, y], [x_interaction, y_interaction], True)
           
            #self._draw_line(x, y, x_obstacle, y_obstacle, OBSTACLE_FORCE__COLOUR)
            pygame.draw.aaline(self.screen, OBSTACLE_FORCE__COLOUR, [x, y], [x_obstacle, y_obstacle], True)
            
            #draw initial position
            self.draw_target(tracked_initial_posistion[0],tracked_initial_posistion[1])
            #add into trajectory
            self.pedestrian_traj_track.append((x,y))
            
            #draw trail line
            if len(self.pedestrian_traj_track) >1:
                for x in range(len(self.pedestrian_traj_track)-1):
                    self._draw_line(self.pedestrian_traj_track[x][0], 
                                    self.pedestrian_traj_track[x][1], 
                                    self.pedestrian_traj_track[x+1][0],
                                    self.pedestrian_traj_track[x+1][1],
                                    TRAIL_COLOUR)
                
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
    
    def get_pos_tracked(self):
        return self.pedestrian_pos_track
    
    def reset_tracked_position(self):
        self.pedestrian_pos_track = [-100.0,-100.0]
         
    def convert_pos_coords(self,x,y):
        
        shift_w = self.width/2
        shift_h = self.height/2
        
        x = (x-shift_w)/self.pixel_factor
        y = (y-shift_h)/self.pixel_factor
        return (x,y)
    
    def is_tracked_pedestrian(self, pos_x, pos_y):
        if self.pedestrian_pos_track[0] == -100.0 and self.pedestrian_pos_track[1] == -100.0:
            return False
        elif hypot(self.pedestrian_pos_track[0]-pos_x, self.pedestrian_pos_track[1]- pos_y) < constants.threshold_track_pedestrian_pos:
            return True
        return False