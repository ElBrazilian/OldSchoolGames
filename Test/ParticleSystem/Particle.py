import pygame
from pygame.locals import *
import types

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
        self._position   = position
        self.position    = V() if type(position) == types.FunctionType else position
        self._direction  = direction
        self._speed      = speed 

        self.lifespan   = lifespan
        self.life       = lifespan
        self.time       = 0

        self._ipos       = position
        self._idir       = direction
        self._ispeed     = speed

        if type(position) == types.FunctionType:
            self._ipos = position(self)
        if type(direction) == types.FunctionType:
            self._idir = direction(self)
        if type(speed) == types.FunctionType:
            self._ispeed = speed(self)

    def direction(self):
        if type(self._direction) == types.FunctionType:
            return self._direction(self)
        else:
            return self._direction

    def speed(self):
        if type(self._speed) == types.FunctionType:
            return self._speed(self)
        else:
            return self._speed

    def update(self, dt):
        if type(self._position) == types.FunctionType:
            self.position = self._position(self)
        else:
            self.position += self.direction() * self.speed() * dt
        self.life -= dt
        self.time += dt

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
        self._color = color
        self.radius = radius
        self.surface = pygame.Surface((self.radius*2, self.radius*2), SRCALPHA)
        self.surface.set_alpha(self.color()[-1])
        self.time = 0
    
    def color(self):
        if type(self._color) == types.FunctionType:
            return self._color(self)
        else:
            return self._color
    def update(self, dt):
        super().update(dt)

    def draw(self, surface):
        #pygame.gfxdraw.filled_circle(surface, int(self.position.x), int(self.position.y), self.radius, self.color)
        self.surface.fill((0))
        pygame.draw.circle(self.surface, self.color()[:3], (self.radius, self.radius), self.radius)
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

