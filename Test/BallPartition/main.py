import pygame
from pygame.locals import *


from lib.BaseScene import BaseScene
from .ExploadedBall import ExploadedBall


class Scene(BaseScene):
    def load(self):
        self.ball = ExploadedBall('Test/BallPartition/ball.json')



    def update(self, dt, events):
        self.ball.update(dt)

        if events.on_first_dump_points:
            self.ball.dump_points('Test/BallPartition/points.json')

    def physics_update(self, dt):
        pass


    def draw(self, fenetre):
        self.ball.draw(fenetre)
