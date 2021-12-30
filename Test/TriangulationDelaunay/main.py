import pygame
from pygame.locals import *

from lib.BaseScene import BaseScene
from lib.Math.Vector import Vector2 as V

import json

from .DelaunayTriangulation import *
from lib.HUD.Canvas import Canvas
from lib.HUD.Label import Label
import math


class Scene(BaseScene):
    def load(self):
        pygame.font.init()
        with open('Test/TriangulationDelaunay/points.json', 'r') as file:
            points = json.loads(file.read())['points']
        self.points = []
        for point in points:
            self.points.append([int(x) for x in point])
        self.all_triangles = []
        self.all_circle_center = []
        self.all_circle_radius = []
        self.res_triangles = []

        # Live options
        self.show_all_triangles = True
        self.auto_update = True
        self.show_points = True
        self.show_all_circles_center = True
        self.show_all_circles = True

        self.update_tri()

        # Draw
        height = 35
        self.font = pygame.font.Font("Test/TriangulationDelaunay/fonts/Oswald.ttf", 22)
        self.canvas = Canvas(self.window, (20,20,20), V(0,0), V(250,height*5)).load()
        self.label_auto_update = Label(self.canvas, self.font, "auto_update (A)", Label.TEXT_CENTERED).set_color(self.options.true_color).set_size(V(0,height)).center_horizontally(height*0).add_to_canvas(self.canvas)
        self.label_show_points = Label(self.canvas, self.font, "show_points (Z)", Label.TEXT_CENTERED).set_color(self.options.true_color).set_size(V(0,height)).center_horizontally(height*1).add_to_canvas(self.canvas)
        self.label_show_all_triangles = Label(self.canvas, self.font, "show_all_triangles (E)", Label.TEXT_CENTERED).set_color(self.options.true_color).set_size(V(0,height)).center_horizontally(height*2).add_to_canvas(self.canvas)
        self.label_show_all_circles_center = Label(self.canvas, self.font, "show_all_circles_center (R)", Label.TEXT_CENTERED).set_color(self.options.true_color).set_size(V(0,height)).center_horizontally(height*3).add_to_canvas(self.canvas)
        self.label_show_all_circles = Label(self.canvas, self.font, "show_all_circles (T)", Label.TEXT_CENTERED).set_color(self.options.true_color).set_size(V(0,height)).center_horizontally(height*4).add_to_canvas(self.canvas)
    
        self.label_show_all_triangles.word_wrapping = False
        self.label_auto_update.word_wrapping = False
        self.label_show_points.word_wrapping = False
        self.label_show_all_circles_center.word_wrapping = False
        self.label_show_all_circles.word_wrapping = False

        self.label_show_all_triangles.load()
        self.label_auto_update.load()
        self.label_show_points.load()
        self.label_show_all_circles_center.load()
        self.label_show_all_circles.load()

        self.pt = (400,50)
        self.isIn = False
        self.i = 0
    
    def update(self, dt, events):
        if events.mouse.left.down_rn:
            self.points.append(list(events.mouse.pos().to_pygame()))
            if self.auto_update:
                self.update_tri()
        if events.mouse.right.down_rn:
            to_remove = []
            for point in self.points:
                if (events.mouse.pos() - V(point)).mag() < self.options.points.del_radius:
                    to_remove.append(point)

            for point in to_remove:
                self.points.remove(point)

            if self.auto_update:
                self.update_tri()
        if events.on_first_save_points:
            text = json.dumps({"points": self.points}, indent=4)
            with open('Test/TriangulationDelaunay/points.json', 'w') as file:
                file.write(text)
            print('saved')
        if events.on_first_clear_all:
            self.points = []
            if self.auto_update:
                self.update_tri()
        if events.on_first_show_all_triangles:
            self.show_all_triangles = not self.show_all_triangles
            self.label_show_all_triangles.set_color(self.options.true_color if self.show_all_triangles else self.options.false_color).load()
        if events.on_first_swap_auto_update:
            self.auto_update = not self.auto_update
            self.label_auto_update.set_color(self.options.true_color if self.auto_update else self.options.false_color).load()
        if events.on_first_show_points:
            self.show_points = not self.show_points
            self.label_show_points.set_color(self.options.true_color if self.show_points else self.options.false_color).load()
        if events.on_first_show_all_circles:
            self.show_all_circles = not self.show_all_circles
            self.label_show_all_circles.set_color(self.options.true_color if self.show_all_circles else self.options.false_color).load()
        if events.on_first_show_all_circles_center:
            self.show_all_circles_center = not self.show_all_circles_center
            self.label_show_all_circles_center.set_color(self.options.true_color if self.show_all_circles_center else self.options.false_color).load()
        
        if events.on_first_update:
            self.update_tri()


    def update_tri(self):
        self.all_circle_radius = []
        self.all_circle_center = []

        points = self.points
        self.res_triangles = delaunay_triangulation(points)


    def physics_update(self, dt):
        pass



    def draw(self, fenetre):
        if self.show_all_triangles:
            for triangle in self.all_triangles:
                a,b,c = triangle
                pygame.draw.line(fenetre, self.options.all_triangles.color, a, b, self.options.all_triangles.width)
                pygame.draw.line(fenetre, self.options.all_triangles.color, b, c, self.options.all_triangles.width)
                pygame.draw.line(fenetre, self.options.all_triangles.color, a, c, self.options.all_triangles.width)

        if self.show_points:
            for point in self.points:
                pygame.draw.circle(fenetre, self.options.points.color, point, self.options.points.radius)

        for i in range(len(self.all_circle_center)):
            pt = self.all_circle_center[i]
            r = self.all_circle_radius[i]

            if self.show_all_circles_center:
                pygame.draw.circle(fenetre, self.options.circles.pt_color, pt, self.options.circles.pt_radius)
            if self.show_all_circles:
                pygame.draw.circle(fenetre, self.options.circles.color, pt, r, self.options.circles.width)
        
        for triangle in self.res_triangles:
            a,b,c = triangle
            pygame.draw.line(fenetre, self.options.res_triangles.color, a, b, self.options.res_triangles.width)
            pygame.draw.line(fenetre, self.options.res_triangles.color, b, c, self.options.res_triangles.width)
            pygame.draw.line(fenetre, self.options.res_triangles.color, a, c, self.options.res_triangles.width)
        self.canvas.draw()