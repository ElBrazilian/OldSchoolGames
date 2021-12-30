
import json, os, math, pygame

from lib.Options import Options
from lib.Math.Vector import Vector2 as V

from lib.Math.DelaunayTriangulation import delaunay_triangulation


class ExploadedBall:
    def __init__(self, ball_options_file):
        self.ball_options_file = ball_options_file
        self.position = V(600,400)


        self.load_options()
        self.load()
        if self.options.check_option_update:
            self.last_update_check = 0
            self.last_option_update = os.path.getmtime(self.ball_options_file)


    def init_vars(self):
        self.points = []
        self.points_as_list = []
        self.triangles = []

    def load(self):
        self.init_vars()

        # Making all the points
        d_alpha = 2*math.pi/self.options.ball.outer_points
        self.points = []
        for i in range(self.options.ball.outer_points):
            alpha = i * d_alpha

            point = V.from_polar(self.options.ball.radius, alpha)
            self.points.append(point)
            self.points_as_list.append(point.to_pygame())
        point = V()
        self.points.append(point)
        self.points_as_list.append(point.to_pygame())


        # Adding inner points

        
        # Computing delaunay triangulation
        self.triangles = delaunay_triangulation(self.points_as_list)
        

    def load_options(self):
        with open(self.ball_options_file) as file:
            options_json = json.loads(file.read())
        self.options = Options(options_json)

    def update(self, dt):


        if self.options.check_option_update:
            self.last_update_check += dt
            if self.last_update_check >= self.options.option_update_check_interval:
                self.last_update_check = 0
                time = os.path.getmtime(self.ball_options_file)
                if time != self.last_option_update:
                    self.last_option_update = time
                    self.load_options()
                    if self.options.full_reload:
                        self.load()

    def dump_points(self, filepath):
        points = []
        for point in self.points_as_list:
            points.append((self.position + V(point)).to_list())
        txt = json.dumps({"points": points}, indent=4)
        with open(filepath, 'w') as file:
            file.write(txt)

    def draw(self, surface):
        if self.options.debug.triangles.show:
            for triangle in self.triangles:
                a, b, c = [V(x) for x in triangle]

                polygon = [(self.position + x).to_pygame() for x in [a, b, c]]
                pygame.draw.polygon(surface, self.options.debug.triangles.color, polygon)
                    
                if self.options.debug.triangles.show_edges:
                    pygame.draw.line(surface, self.options.debug.triangles.edge_color, (self.position + a).to_pygame(), (self.position + b).to_pygame(), self.options.debug.triangles.edge_width)
                    pygame.draw.line(surface, self.options.debug.triangles.edge_color, (self.position + b).to_pygame(), (self.position + c).to_pygame(), self.options.debug.triangles.edge_width)
                    pygame.draw.line(surface, self.options.debug.triangles.edge_color, (self.position + c).to_pygame(), (self.position + a).to_pygame(), self.options.debug.triangles.edge_width)
        
        if self.options.debug.points.show:
            for point in self.points:
                pygame.draw.circle(surface, self.options.debug.points.color, (self.position + point).to_pygame(), self.options.debug.points.radius)