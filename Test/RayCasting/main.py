import pygame
from pygame.locals import *

from lib.BaseScene import BaseScene
from lib.Math.Vector import Vector2 as V
import json

from .RayCasting import *

class Scene(BaseScene):
    def load(self):
        self.dir = V(1,0)
        self.position = V()

        self.start_pos = None
        with open('Test/RayCasting/edges.json') as file:
            edges = json.loads(file.read())['edges']

        self.edges = []
        for edge in edges:
            a = V(*(edge[0]))
            b = V(*(edge[1]))
            self.edges.append([a,b])

        self.inter = None
        self.all_inters = []


    def update(self, dt, events):
        mouse_pos = events.mouse.pos()
        if events.mouse.left.down:
            if (mouse_pos - self.position) != V():
                self.dir = (mouse_pos - self.position).normalize()
        else:
            self.position = mouse_pos

            
        if events.mouse.right.down_rn:
            if self.start_pos == None:
                self.start_pos = mouse_pos
            else:
                self.edges.append([self.start_pos, mouse_pos])
                self.start_pos = None

        if events.on_first_clear:
            self.edges = []
        if events.on_first_save:
            edges = []
            for edge in self.edges:
                a, b = edge
                new_a = [a.x, a.y]
                new_b = [b.x, b.y]
                edges.append([new_a, new_b])

            data = json.dumps({'edges':edges}, indent=4)
            with open('Test/RayCasting/edges.json', 'w') as file:
                file.write(data)
            print('saved')

    def physics_update(self, dt):
        self.inter, self.all_inters = ray_casting(self.position, self.dir, self.edges)

    def draw(self, fenetre):
        if self.start_pos != None:
            pygame.draw.circle(fenetre, self.options.start_pos.color, self.start_pos.to_pygame(), self.options.start_pos.radius)
        
        for edge in self.edges:
            pygame.draw.line(fenetre, self.options.edges.color, edge[0].to_pygame(), edge[1].to_pygame(), self.options.edges.width)

        pygame.draw.line(fenetre, self.options.dir.color, self.position.to_pygame(), (self.position + self.dir * self.options.dir.length).to_pygame(), self.options.dir.width)
        pygame.draw.circle(fenetre, self.options.player.color, self.position.to_pygame(), self.options.player.radius)
        
        if self.options.all_inter.show:
            for inter in self.all_inters:
                if inter != self.inter:
                    pygame.draw.circle(fenetre, self.options.all_inter.color, inter.to_pygame(), self.options.all_inter.radius)

        if self.inter != None:
            pygame.draw.circle(fenetre, self.options.inter.color, self.inter.to_pygame(), self.options.inter.radius)