import pygame
from pygame.locals import *

from lib.BaseScene import BaseScene

from lib.HUD.Canvas import Canvas
from lib.HUD.Button import Button
from lib.HUD.RoundedRect import RoundedRect
from lib.Math.Vector import Vector2 as V

from Pong.Game.Player import Player
from Pong.Game.Ball import Ball



class Scene(BaseScene):
    def load(self):
        def load_players():
            # compute size, position...
            self.playerA = Player(
                self.game, 'a',
                V(
                    self.options.players.center_x_offset,
                    (1-self.options.players.size[1])/2
                ),
                self.options.players.size,
                self.options.players.colorA,
                self.options.players.radius_as_width_ratio,
                self.options.players.speed, 
                self.options.players.y_margin
            ).load()
            self.playerB = Player(
                self.game, 'b',
                V(
                    1 - self.options.players.size[0] - self.options.players.center_x_offset,
                    (1-self.options.players.size[1])/2
                ),
                self.options.players.size,
                self.options.players.colorB,
                self.options.players.radius_as_width_ratio,
                self.options.players.speed, 
                self.options.players.y_margin
            ).load()
        ###

        self.game = Canvas(self.window, self.options.background_color).fit().center().load()
        load_players()
        self.game.append_child(self.playerA)
        self.game.append_child(self.playerB)

        # Load ball
        self.ball = Ball(self.game, V(self.options.ball.starting_x,self.options.ball.starting_y), V(1,0), self.options.ball.radius, self.options.ball.color, self.options.ball.speed)
        self.game.append_child(self.ball)

        self.test = pygame.Surface((self.window.get_size()))
        self.test.fill((255,0,0))
        



    def update(self, dt, events):
        self.test.fill((0,0,0))
        self.playerA.update(dt, events)
        self.playerB.update(dt, events)
        self.ball.update(dt, events)

        if events.mouse.left.click_rn:
            print('hey')

    def physics_update(self, dt):
        pass


    def draw(self, fenetre):
        self.game.draw()

