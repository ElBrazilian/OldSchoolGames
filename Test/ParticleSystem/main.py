import pygame
from pygame.locals import *

from lib.BaseScene import BaseScene

import pygame.gfxdraw
import numpy as np

class Scene(BaseScene):
    def load(self):
        self.num_pixels = 900
        self.m = self.app.options.window.height
        self.pixels = np.random.randint(0,self.m, (self.num_pixels,2))

        self.surface = pygame.Surface((self.app.options.window.width,self.app.options.window.height), SRCALPHA)
        


    def update(self, dt, events):
        pass

    def physics_update(self, dt):
        pass


    def draw(self, fenetre):
        bandwidth = self.app.options.window.width // 256
        # Line by line drawing: down to 60 FPS

        # Pixel with fill(..(1,1)) : 1.56 FPS
        # Pixel with line start=end : 1.33 FPS
        # Pixel with surface.set_at : 2.17 FPS
        # Pixel with pixel_array : 2.18 FPS
        # Pixel with circle radius0 : 2.00 FPS

        # 900 1pixel radius gfx: 410 FPS
        # 900 1pixel radius draw: 300 FPS mais plus beau
        # 900 set_at: 380-400 FPS
        
        self.surface.fill((255,50,50))
        for pixel in self.pixels:
            self.surface.set_at(pixel, (255,0,0,0))

        print(self.surface)
        self.surface.blit(surface, (0,0))
            

        
    #pygame.gfxdraw.filled_circle(fenetre, 100,100,30,(255,0,0))
