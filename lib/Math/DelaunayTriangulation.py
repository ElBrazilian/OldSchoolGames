
from lib.Math.Vector import Vector2 as V
from itertools import combinations

def list_all_triangles(points):
    return list(combinations(points, 3))

def point_in_triangle(p, a, b, c):
    p, a, b, c = V(p), V(a), V(b), V(c)
    def sign(a,b,c):
        return (a.x - c.x)*(b.y-c.y)-(b.x-c.x)*(a.y-c.y)

    d1 = sign(p,a,b)
    d2 = sign(p,b,c)
    d3 = sign(p,c,a)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)

def compute_coeffs(A, B):
    A = V(A)
    B = V(B)

    a = 2*(B.x - A.x)
    b = 2*(B.y - A.y)
    c = A.x ** 2 + A.y ** 2 - B.x ** 2 - B.y ** 2

    return a,b,c

# def compute_circumcircle(triangle):
#     """
#     returns the center as V(x, y) and the radius squared
#     """
#     A,B,C = [V(x) for x in triangle]
#     a1,b1,c1 = compute_coeffs(A, B)
#     a2,b2,c2 = compute_coeffs(A, C)

#     x = (-c1*b2+c2*b1)/(a1*b2-b1*a2)
#     y = (-c2*a1+c1*a2)/(a1*b2-b1*a2)

#     r2 = (x-A.x)**2 + (y-A.x)**2
#     return [x,y], r2

def compute_circumcircle(triangle):
    a,b,c = triangle
    ad = a[0] * a[0] + a[1] * a[1]
    bd = b[0] * b[0] + b[1] * b[1]
    cd = c[0] * c[0] + c[1] * c[1]
    D = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
    
    x = (1 / D * (ad * (b[1] - c[1]) + bd * (c[1] - a[1]) + cd * (a[1] - b[1])))
    y = (1 / D * (ad * (c[0] - b[0]) + bd * (a[0] - c[0]) + cd * (b[0] - a[0])))

    r2 = (x-a[0]) ** 2 + (y-a[1])**2
    return [x, y], r2



def compute_super_triangle(points):
    espilon = 10
    if len(points) == 0:
        return [[0,0],[0,0],[0,0]]

    maxY = max(points, key=lambda x: x[1])[1] 
    minY = min(points, key=lambda x: x[1])[1]  
    minX = min(points, key=lambda x: x[0])[0] 
    maxX = max(points, key=lambda x: x[0])[0] 

    offset = (maxX - minX) / 2
    A,B,C = V(),V(),V()
    # A: bas gauche
    # B: bas droite
    # C: milieu haut

    A.x = minX - offset
    B.x = maxX + offset
    A.y = maxY + espilon
    B.y = maxY + espilon

    if minY == maxY: # Si les pts sont en lignes
        C.x = (maxX+minX)/2
        C.y = minY - offset
    else:
        C.x = (maxX+minX)/2
        C.y = maxY - 2 * (maxY-minY) - 3*espilon
         
    return [list(D.to_pygame()) for D in [A,B,C]]

def inside_circumcircle(point, triangle):
    """
    Checks if a point is in the circumcircle of the given triangle
    """
    center, rayon_c = compute_circumcircle(triangle)
    return (V(center) - V(point)).mag_sqr() <= rayon_c
def edges(triangle):
    return [
        [triangle[0], triangle[1]],
        [triangle[1], triangle[2]],
        [triangle[2], triangle[0]]
    ]

def remove_super_triangle(triangles, super_triangle):
    """
    Removes all triangles sharing a vertex with the super_triangle

    """
    def point_in_common(triangleA, triangleB):
        for point1 in triangleA:
            for point2 in triangleB:
                if point1 == point2:
                    return True
        return False

    res = []
    for triangle in triangles:
        if not point_in_common(triangle, super_triangle):
            res.append(triangle)
    return res

def delaunay_triangulation(points):
    """
    Creates the delaunay triangulation of a list of points (as list of int/float)
    returns a list of triangles
    """
    if len(points) < 3:
        return []

    super_triangle = compute_super_triangle(points)
    triangulation = [super_triangle]
    for point in points:
        bad_triangles = []
        for triangle in triangulation:
            if inside_circumcircle(point, triangle):
                bad_triangles.append(triangle)
        
        polygon = []
        for triangle in bad_triangles:
            for edge in edges(triangle):
                is_shared = False
                for other_triangle in bad_triangles:
                    if triangle == other_triangle:
                        continue
                        
                    for other_edge in edges(other_triangle):
                        if (edge[0] == other_edge[0] and edge[1] == other_edge[1]) or (edge[1] == other_edge[0] and edge[0] == other_edge[1]):
                            is_shared = True

                if not is_shared:
                    polygon.append(edge)
        
        for triangle in bad_triangles:
            triangulation.remove(triangle)

        for edge in polygon:
            triangulation.append([point,edge[0],edge[1]])
    return remove_super_triangle(triangulation, super_triangle)