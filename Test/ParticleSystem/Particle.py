import pygame
from pygame.locals import *

from lib.Math.Vector import Vector2 as V

class Particle:
    """
    Arguments:
        - position      [Vector2]   : initial position
        - direction     [Vector2]   : initial direction (norm = 1)
        - speed         [float]     : speed as px/s

    Variables:
        - arguments

    Methods:
        - 
    """
    def __init__(self, position: Vector2, direction: Vector2, speed:float):
        self.position   = position
        self.direction  = direction
        self.speed      = speed 