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
        self.w = w

        self.A = V(x+w/2, y+w/2)
        self.B = V(x+w/2, y + h - w/2)

        self.axis_proj = None

        self.target = V(100,400)

        self.ball = BaseBall(V(0,0), V(1,0), 10, [0,0,255], 5000)


    def update(self, dt, events):
        if events.mouse.left.down_rn:
            vel_dir = - (events.mouse.pos() - self.target).normalize()
            self.ball = BaseBall(events.mouse.pos(), vel_dir, 10, [50,50,255], 500)
            


    def physics_update(self, dt):
        self.ball.update(dt)
        d, self.axis_proj = distance_and_proj_point_to_segment(self.ball.position, self.A, self.B)
        
        if d <= self.ball.radius + self.w/2:
            # if it hits, revert the move
            self.ball.position += self.ball.velocity * (-dt) * self.ball.speed 
            self.stopPos = V(self.ball.position)

            # stop ball, change color
            self.ball.color = (0,255,0)

            # calculate normal, ..
            self.normal = (self.ball.position - self.axis_proj).normalize()
            self.projection = - self.normal * self.ball.velocity.dot(self.normal) # projection of -vel on the normal
            
            
            self.tmpO = self.ball.position
            self.tmpB = self.tmpO - self.ball.velocity * 50
            self.tmpP = self.tmpO + self.projection * 50
            self.tmpOut = self.tmpB + (self.tmpP - self.tmpB) * 2
            self.ball.velocity = (self.tmpOut - self.tmpO).normalize()
            #self.side_proj = self.axis_proj + (self.ball.position - self.axis_proj)


    def draw(self, fenetre):
        self.rect.draw()
        pygame.draw.circle(fenetre, [255, 0,0], self.A.to_pygame(), 10)
        pygame.draw.circle(fenetre, [0, 255,0], self.B.to_pygame(), 10)
        
        if self.ball.speed == 0:
            pygame.draw.circle(fenetre, [0, 0,255], self.axis_proj.to_pygame(), 5)

            pygame.draw.line(fenetre, [255,0,0], self.tmpO.to_pygame(), self.tmpP.to_pygame(), 2)
            pygame.draw.line(fenetre, [0,255,0], self.tmpO.to_pygame(), self.tmpB.to_pygame(), 2)
            pygame.draw.line(fenetre, [0,0,255], self.tmpO.to_pygame(), self.tmpOut.to_pygame(), 2)


        self.ball.draw(fenetre)

    
