
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

def compute_circomcircle(triangle):
    """
    returns the center as (x, y) and the radius squared
    """
    A,B,C = triangle
    a1,b1,c1 = compute_coeffs(A, B)
    a2,b2,c2 = compute_coeffs(A, C)

    x = (-c1*b2+c2*b1)/(a1*b2-b1*a2)
    y = (-c2*a1+c1*a2)/(a1*b2-b1*a2)

    r2 = (x-A[0])**2 + (y-A[1])**2
    return (x,y), r2

def compute_super_triangle(points):
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
    A.y = maxY
    B.y = maxY

    if minY == maxY: # Si les pts sont en lignes
        C.x = (maxX+minX)/2
        C.y = minY - offset
    else:
        C.x = (maxX+minX)/2
        C.y = maxY - 2 * (maxY-minY)
    return [D.to_pygame() for D in [A,B,C]]