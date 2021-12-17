import pygame
from pygame.locals import *

from lib.BaseScene import BaseScene

from lib.HUD.Canvas import Canvas
from lib.HUD.Button import Button
from lib.HUD.RoundedRect import RoundedRect
from lib.Math.Vector import Vector2 as V

from lib.Math.distance import distance_and_proj_point_to_segment

class Ball:
    def __init__(self, game, position, velocity, radius, color, speed):
        """
        Arguments:
            - game          [HUD/Canvas]        : the game's canvas
            - position      [Lib/Vector2]       : the position of the center, as percents
            - velocity      [Lib/Vector2]       : the velocity of the center, at the start, as percents
            - radius        [float]             : the radius of the ball, as percents of diag
            - color         [tuple(3*int)]      : color, as rgb(0,255)
            - speed         [float]             : speed of the ball, as %diag/s

        Variables:
            same as args
            - rect      [HUD/RoundedRect]   : the actual "sprite", a rect, containing position etc
        """
        self.game = game
        self.position_prc = position
        self.velocity = velocity.normalize()
        self.radius_prc = radius
        self.color = color
        self.speed_prc = speed
        self.compute_prc()

    def compute_prc(self):
        self.position = self.position_prc * self.game.size

        diag = self.game.size.mag()
        self.radius = self.radius_prc * diag
        self.speed =  self.speed_prc * diag

    def load(self):
        pass

    def update(self, dt, events, collide_players):
        self.position += self.velocity * self.speed * dt

        # Collide with the player
        for player in collide_players:
            d, axis_proj = distance_and_proj_point_to_segment(self.position, player.A(), player.B())
            
            if d <= self.radius + player.rect.size.x/2:
                # if it hits, revert the move
                
                normal = (self.position - axis_proj).normalize()
           
                # push it to the side
                self.position = axis_proj + normal * player.rect.size.x * 1.05
                
                normal = (self.position - axis_proj).normalize()
                projection = - normal * self.velocity.dot(normal) # projection of -vel on the normal

                tmpO = self.position
                tmpB = tmpO - self.velocity
                tmpP = tmpO + projection
                tmpOut = tmpB + (tmpP - tmpB) * 2
                self.velocity = (tmpOut - tmpO).normalize()
                
                break

        # Collide top/down
        if self.position.y <= self.radius:
            self.position.y = self.radius
            self.velocity.y = -self.velocity.y
        elif self.position.y + self.radius >= self.game.size.y:
            self.position.y = self.game.size.y - self.radius
            self.velocity.y *= -1

    def draw(self):
        pygame.draw.circle(self.game.surface, self.color, self.position.to_pygame(), self.radius)


class BaseBall:
    def __init__(self, pos, vel, radius, color, speed):
        self.position = pos
        self.ipos = pos
        self.velocity = vel
        self.ivel = -vel
        self.radius = radius
        self.color = color
        self.speed = speed


    def draw(self, fenetre):
        pygame.draw.circle(fenetre, self.color, self.position.to_pygame(), self.radius)

    def update(self, dt):
        self.position += self.velocity * dt * self.speed
    
    def check_collision(self, player, dt):
        self.speed = 0
