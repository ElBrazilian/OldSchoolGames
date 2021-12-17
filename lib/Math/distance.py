from math import sqrt

from lib.Math.Vector import Vector2 as V

def sqr_distance(a, b):
    """
    Calculate the square of the distance from point a to point b

    Arguments:
        - a     [lib/Vector2]   : point
        - b     [lib/Vector2]   : point

    Output:
        - the square of the distance from point a to point b

    """

    return (a-b).mag_sqr()
def distance(a, b):
    """
    Calculate the distance from point a to point b

    Arguments:
        - a     [lib/Vector2]   : point
        - b     [lib/Vector2]   : point

    Output:
        - the distance from point a to point b

    """

    return (a-b).mag()

def distance_from_point_to_segment(m, a, b):
    """
    Calculate the distance from point m to the segment [ab]

    Arguments:
        - m     [lib/Vector2]   : a point
        - a     [lib/Vector2]   : starting point of a segment
        - b     [lib/Vector2]   : ending point of a segment

    Output:
        - the square of the distance from point m to the segment [ab]

    """

    ai = complex(a.x, a.y)
    bi = complex(b.x, b.y)
    mi = complex(m.x, m.y)

    z = (mi-ai)/(bi-ai)
    if 0 <= z.real <= 1:
        return abs(z.imag * (bi-ai))
    else:
        da, db = (b-m).mag_sqr(), (a-m).mag_sqr()
        return sqrt(min(da,db))