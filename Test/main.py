import pygame
from pygame.locals import *

from lib.BaseScene import BaseScene
from lib.Math.distance import *
from lib.Math.Vector import Vector2 as V
from lib.HUD.RoundedRect import RoundedRect

from Pong.Game.Ball import BaseBall

import time

class Scene(BaseScene):
    def load(self):
        x = 400
        y = 100
        w = 100
        h = 500
        self.rect = RoundedRect(
            self.window, V(x,y), V(w, h), [255,255,255], w/2
        ).load()
        self.A = V(x+w/2, y+w/2)
        self.B = V(x+w/2, y + h - w/2)
        self.N = V()
        self.M = V()
        self.w = w

        self.ball = BaseBall(V(0,0), V(1,0), 10, [255,0,0], 10)


    def update(self, dt, events):
        self.M = events.mouse.pos()
        self.M = V(600, 100)

        d, self.N = distance_and_proj_point_to_segment(self.M, self.A, self.B)


    def physics_update(self, dt):
        pass


    def draw(self, fenetre):
        self.rect.draw()
        pygame.draw.circle(fenetre, [255, 0,0], self.A.to_pygame(), 10)
        pygame.draw.circle(fenetre, [0, 255,0], self.B.to_pygame(), 10)
        pygame.draw.circle(fenetre, [0, 0,255], self.N.to_pygame(), 5)
        



        self.ball.draw(fenetre)


        dir = (self.M - self.N).normalize()
        orthog = V(-dir.y, dir.x)
        newn = self.N + dir * self.w/2
        pygame.draw.line(fenetre, [100,100,100], self.N.to_pygame(), (self.N + dir * 100).to_pygame(), 4)
        pygame.draw.line(fenetre, [255,0,0], (newn - orthog*50).to_pygame(), (newn + orthog * 50).to_pygame(), 4)

