import pygame

def circumcenter(a, b, c):
    ad = a[0] * a[0] + a[1] * a[1]
    bd = b[0] * b[0] + b[1] * b[1]
    cd = c[0] * c[0] + c[1] * c[1]
    D = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
    return pygame.Vector2((1 / D * (ad * (b[1] - c[1]) + bd * (c[1] - a[1]) + cd * (a[1] - b[1])),
                           1 / D * (ad * (c[0] - b[0]) + bd * (a[0] - c[0]) + cd * (b[0] - a[0]))))

def LineIsEqual(line1,line2):
    if (line1[0] == line2[0] and line1[1] == line2[1]) or (line1[0] == line2[1] and line1[1] == line2[0]):
        return True
    return False

def distance(point1,point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

class Triangle:
    def __init__(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c
        self.edges = [[self.a,self.b],
                      [self.b,self.c],
                      [self.c,self.a]]
        self.circumcenter = circumcenter(a,b,c)
    def IsPointInCircumcircle(self,point):
        if (self.a.distance_to(self.circumcenter) > point.distance_to(self.circumcenter)):
            return True
        return False
    def HasVertex(self,point):
        if (self.a == point) or (self.b == point) or (self.c == point):
            return True
        return False
    def Show(self,screen,colour):
        for edge in self.edges:
            pygame.draw.aaline(screen,colour,edge[0],edge[1])


from .DelaunayTriangulation import compute_super_triangle
def DelaunayTriangulation(points):
    superTriangle = Triangle(*[pygame.Vector2(p) for p in compute_super_triangle(points)])
    points = [pygame.Vector2(point) for point in points]

    triangulation = []
    triangulation.append(superTriangle)

    for point in points:

        badTriangles = []
        for triangle in triangulation:
            if triangle.IsPointInCircumcircle(point):
                badTriangles.append(triangle)

        polygon = []
        for triangle in badTriangles:
            for triangleEdge in triangle.edges:
                isShared = False
                for other in badTriangles:
                    if triangle == other:
                        continue
                    for otherEdge in other.edges:
                        if LineIsEqual(triangleEdge,otherEdge):
                            isShared = True
                if isShared == False:
                    polygon.append(triangleEdge)

        for badTriangle in badTriangles:
            triangulation.remove(badTriangle)

        for edge in polygon:
            newTriangle = Triangle(edge[0],edge[1],point)
            triangulation.append(newTriangle)

    for triangle in triangulation:
        if triangle.HasVertex(superTriangle.a) and triangle in triangulation:
            triangulation.remove(triangle)
        if triangle.HasVertex(superTriangle.b) and triangle in triangulation:
            triangulation.remove(triangle)
        if triangle.HasVertex(superTriangle.c) and triangle in triangulation:
            triangulation.remove(triangle)

    return triangulation