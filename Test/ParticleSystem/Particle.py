import pygame
from pygame.locals import *

import pygame.gfxdraw

from lib.Math.Vector import Vector2 as V

class Particle:
    """
    Arguments:
        - position      [Vector2]   : initial position
        - direction     [Vector2]   : initial direction (norm = 1)
        - speed         [float]     : speed as px/s
        - lifespan      [float]     : lifespan of the particle, in seconds
        - color         [list(int)] : color as rgba 255

    Variables:
        - arguments
        - life          [float]     : remaining lifespan

    Methods:
        - reset         [arguments] : reset the particle (works as __init__) in order not to create a new one
    """
    def __init__(self, position, direction, speed:float, lifespan: float):
        self.reset(position, direction, speed, lifespan)

    def reset(self, position, direction, speed:float, lifespan: float):
        self.position   = position
        self.direction  = direction
        self.speed      = speed 

        self.lifespan   = lifespan
        self.life       = lifespan


    def update(self, dt):
        self.position += self.direction * self.speed * dt
        self.life -= dt

    def __str__(self):
        return '<Particle>'
    def __repr__(self):
        return '<Particle>'


class RoundParticle(Particle):
    """
    Arguments:
        - same as particle
        - color     [list(int)]     : color as rgba 255
        - radius    [int]           : radius of the particle

    """
    def __init__(self, position, direction, speed:float, lifespan: float, color, radius):
        self.reset(position, direction, speed, lifespan, color, radius)

    def reset(self, position, direction, speed:float, lifespan: float, color, radius):
        super().reset(position, direction, speed, lifespan)
        self.color = color
        self.radius = radius
        self.surface = pygame.Surface((self.radius*2, self.radius*2), SRCALPHA)
        pygame.draw.circle(self.surface, self.color[:3], (self.radius, self.radius), self.radius)
        self.surface.set_alpha(self.color[-1])
        self.t = 0
    
    def update(self, dt):
        self.position += self.direction * self.speed * dt
        self.life -= dt
        self.t += dt

    def draw(self, surface):
        #pygame.gfxdraw.filled_circle(surface, int(self.position.x), int(self.position.y), self.radius, self.color)
        surface.blit(self.surface, (self.position.x - self.radius, self.position.y - self.radius))

class ParticleTemplate(Particle):
    """
    Arguments:
        - same as particle
        - color     [list(int)]     : color as rgba 255
        - radius    [int]           : radius of the particle

    """
    def __init__(self, position, direction, speed:float, lifespan: float):
        super().__init__(position, direction, speed, lifespan)
        
    
    def update(self, dt):
        
        self.position += self.direction * self.speed * dt
        self.life -= dt

    def draw(self, surface):
        pass

