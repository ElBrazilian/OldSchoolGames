from lib.Math.Vector import Vector2 as V
import numpy as np



def segment_intersect(point, dir, edge, threshold=2):
    """
    Arguments:
        - point [Vector2]: the start of the ray
        - dir   [Vector2]: the dir   of the ray
        - edge  [list(Vector2, Vector2)]: a segment where to cast the ray
        - threshold [float]: the threshold for the lines to be considered para

    returns the intersection point as a Vector2, or None if no intersection found
    """
    
    tmp_length = 10
    
    x1, y1 = point.to_list()
    x2, y2 = (point + dir * tmp_length).to_list()

    x3, y3 = edge[0].to_list()
    x4, y4 = edge[1].to_list()

    D = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if -threshold <= D <= threshold:
        return

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4))/D
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2))/D

    if t >= 0 and 0 <= u <= 1:
        # intersection found
        return point + dir * t * tmp_length
    else:
        return

def ray_casting(point, dir, edges, threshold=2):
    """
    Arguments:
        - point [Vector2]: the start of the ray
        - dir   [Vector2]: the dir   of the ray
        - edges  [list(list(Vector2, Vector2))]: all the edges
        - threshold [float]: the threshold for the lines to be considered para

    returns:
        - the clothest point as a vector2
        - all the intersection points
    """

    all_intersect = []
    clothest = None
    clothest_dist_squared = float('inf')

    for edge in edges:
        intersect = segment_intersect(point, dir, edge, threshold)
        if intersect != None:
            all_intersect.append(intersect)
            dist_squared = (intersect - point).mag_sqr()
            if dist_squared <= clothest_dist_squared:
                clothest_dist_squared = dist_squared
                clothest = intersect


    return clothest, all_intersect