import pygame
from pygame.locals import *

from lib.BaseScene import BaseScene

from lib.HUD.Canvas import Canvas
from lib.HUD.Button import Button
from lib.HUD.RoundedRect import RoundedRect
from lib.Math.Vector import Vector2 as V

from lib.Math.distance import distance_from_point_to_segment

class Player:
    def __init__(self, game, player, position, size, color, radius_ratio, speed, margin):
        """
        Arguments:
            - game          [HUD/Canvas]        : the game's canvas
            - player        [str]               : the player, a or b
            - position      [Lib/Vector2]       : the position of the top left corner, as percents
            - size          [Lib/Vector2]       : the size of the player, as percents
            - color         [tuple(3*int)]      : color, as rgb(0,255)
            - radius_ratio  [float]             : rect's corner radius
            - speed         [float]             : speed of the player, as %height/s
            - margin        [float]             : top and bottom margin, as %height

        Variables:
            same as args
            - rect      [HUD/RoundedRect]   : the actual "sprite", a rect, containing position etc
        """
        self.game = game
        self.rect = RoundedRect(game).set_position_ratio(V(position)).set_size_from_ratio(V(size)).set_color(color).set_radius_from_ratio(radius_ratio)
        self.speed = speed
        self.margin = margin
        self.player = player.lower()

        #self.m_pos = V(0,0)

    def load(self):
        self.rect.load()
        return self

    def A(self):
        return V(self.rect.position.x+self.rect.size.x/2, self.rect.position.y+self.rect.size.x/2)
        
    def B(self):
        return V(self.rect.position.x+self.rect.size.x/2, self.rect.position.y + self.rect.size.y - self.rect.size.x/2)

    def update(self, dt, events):
        dy = dt * self.speed * self.game.size.y
        if events[f'up_{self.player}']: self.rect.position.y = max(self.margin*self.game.size.y,self.rect.position.y - dy)
        if events[f'down_{self.player}']: self.rect.position.y = min((1-self.margin)*self.game.size.y - self.rect.size.y, self.rect.position.y + dy)

    def draw(self):
        self.rect.draw()

        # test if distnace works
        # if self.player == 'a':
        #     w, h = self.rect.size.x, self.rect.size.y
        #     a = self.rect.position + V(w/2,w/2)
        #     b = self.rect.position + V(w/2,h-w/2)
        #     color = (0,255,0)
        #     r = 10
        #     if distance_from_point_to_segment(self.m_pos, a, b) < w/2 + r:
        #         color = (255,0,0)
        #     pygame.draw.line(self.rect.parent.surface, (255,0,0), a.to_pygame(), b.to_pygame())
        #     pygame.draw.circle(self.rect.parent.surface, color, self.m_pos.to_pygame(), r)
            