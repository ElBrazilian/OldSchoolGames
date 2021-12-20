import pygame
from pygame.locals import *

from lib.BaseScene import BaseScene

import pygame.gfxdraw
import numpy as np

from lib.Math.Vector import Vector2 as V

from .Particle import Particle
from .ParticlePool import ParticlePool
from .ParticleSystem import ParticleSystem
from .Emitter import *

class Scene(BaseScene):
    def load(self):

        self.surface = pygame.Surface((self.app.options.window.width,self.app.options.window.height), SRCALPHA)

        self.system = ParticleSystem()
        self.emitter = LinearEmitter(self.system, 2, V(self.app.options.window.width/2,self.app.options.window.height/2), V(0,-1),400,3, (0,0,0,25), 20)
        self.system.add_emitter(self.emitter)

    def update(self, dt, events):
        self.system.update(dt)

    def physics_update(self, dt):
        pass


    def draw(self, fenetre):

        # Line by line drawing: down to 60 FPS

        # Pixel with fill(..(1,1)) : 1.56 FPS
        # Pixel with line start=end : 1.33 FPS
        # Pixel with surface.set_at : 2.17 FPS
        # Pixel with pixel_array : 2.18 FPS
        # Pixel with circle radius0 : 2.00 FPS

        # 900 1pixel radius gfx: 410 FPS
        # 900 1pixel radius draw: 300 FPS mais plus beau
        # 900 set_at: 380-400 FPS

        self.surface.fill(self.options.background_color)
        self.system.draw(self.surface)
        fenetre.blit(self.surface, (0,0))
            
        #print(self.emitter.pool.particles)
        
