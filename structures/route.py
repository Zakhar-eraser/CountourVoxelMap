import numpy as np
from utils.grids.occupancy_grid import qidx2pos
from utils.grids.occupancy_grid import qvect_idx2pos

class Route:
    """List with array of points to destinate next point as value"""
    
    def __init__(self):
        self.next_point = None
        self.prev_point = None
        self.point = None
        self.visit_points = []
        self.observe_points = []

def route_idx2pos(route_idx):
    route = Route()
    proute = route
    while route_idx is not None:
        proute.point = qidx2pos(route_idx.point)
        proute.visit_points = list(qvect_idx2pos(route_idx.visit_points))
        proute.observe_points = list(qvect_idx2pos(route_idx.observe_points))
        route_idx = route_idx.next_point
        if route_idx is not None:
            proute.next_point = Route()
            proute = proute.next_point
    
    return route

def route2array(route):
    points = []
    while route is not None:
        points.append(route.point)
        points += route.visit_points
        route = route.next_point
    
    return np.array(points)
