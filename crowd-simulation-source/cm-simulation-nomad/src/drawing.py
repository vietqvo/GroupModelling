'''
Created on 13 Feb 2015

@author: quangv
'''
import pygame
from pygame import gfxdraw
import sys

BG_WHITE_COLOUR = (255,255,255)
DRAW__DARK_COLOUR = (0,0,0)
TARGET_PINK__COLOUR = (255,0,127)

START_AREA_COLOUR = (148,154,70)
COLOURS = [
        (102,204,0), # green color
        (255,0,0), # red color
        (0,0,255), # blue color
        (0,0,0)
        ]
class Canvas:
    """This class is to manage canvas and its object """
    def __init__(self, width, height, factor, image_prefix):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption("Pedestrian Types_ Nomad Model")
        self.pixel_factor = factor
        self.image_prefix = image_prefix
        self.target_colours = dict()
        self.font = pygame.font.Font(None, 18)
        self.clock = pygame.time.Clock()

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
        pygame.image.save(self.screen, "%s-%05d.%s" % (self.image_prefix, frames, ext))
        
    def _draw_circle(self, x, y, radii, color):
        gfxdraw.aacircle(self.screen, x, y, radii, color)
        #pygame.draw.circle(self.screen, color, (x,y), radii, 1)
        #try:
        #    gfxdraw.aacircle(self.screen, x, y, radii, color)    
        #except:
            #print("OverflowError when drawing pedestrian: signed short integer is less than minimum")
        #    sys.exit()
        
    def _draw_line(self, x1, y1, x2, y2, c):
        gfxdraw.line(self.screen, x1, y1, x2, y2, c)
        #pygame.draw.line(self.screen, c, (x1, y1), (x2, y2))

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
        
    def draw_pedestrian(self, x, y, r, t): 
        colour = COLOURS[int(round(t))]
        (x,y) = self.screen_coords(x,y)
        self._draw_circle(x, y, self.screen_radius(r), colour)
        
    def draw_target(self, x, y):
        (x,y) = self.screen_coords(x,y)
        if x > self.width or x < -self.width or y > self.height or y < -self.height:
            return
        
        pygame.draw.line(self.screen, TARGET_PINK__COLOUR, (x, self.height), (x, (-1)*self.height))
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
        y *= -self.pixel_factor

        shift_w = self.width/2
        shift_h = self.height/2

        x += shift_w
        y += shift_h

        return (int(x),int(y))

    def screen_radius(self, r):
        return int(r*self.pixel_factor)    