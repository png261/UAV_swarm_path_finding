from enum import Enum
from Parameters import Parameters
from utils import is_point_in_polygon, Vector, Point
import random

class Map:
    """
        Map class to represent the map of the area of interest
        Attributes:
            aoi: Area of Interest, List of cell positition
            wind: Wind direction, Vector object
            num_of_obstacles: Number of obstacles to be rendered
            priority: 2D array to store the priority of each cell, dim: (map_width, map_height)
            state: 2D array to store the state of each cell, dim: (map_width, map_height)
            CellState: Enum to represent the state of a cell
    """
    class CellState:
        NOT_SCANNED = 1
        SCANNED = 2
        UNREACHABLE = -1
        NO_INTEREST = 0

    def __init__(self, aoi, wind, num_of_obstacles):
        self.aoi = aoi
        self.wind = wind
        self.num_of_obstacles = num_of_obstacles
        self.priority = [[0 for j in range(Parameters.map_height)] for i in range(Parameters.map_width)]
        self.state = [[Map.CellState.NO_INTEREST for j in range(Parameters.map_height)] for i in range(Parameters.map_width)]

        for x in range(Parameters.map_width):
            for y in range(Parameters.map_height):
                if is_point_in_polygon(x, y, aoi):
                    self.state[x][y] = Map.CellState.NOT_SCANNED 
                else:
                    self.state[x][y] = Map.CellState.NO_INTEREST

        
        all_points = [(x, y) for x in range(Parameters.map_width) for y in range(Parameters.map_height)]
        points = random.sample(all_points, num_of_obstacles)
        for x, y in points:
            self.state[x][y] = Map.CellState.UNREACHABLE

    def top_left_corner_of_the_cell(self, x, y):
        """
            Args:
                x: x-coordinate of the cell in the map
                y: y-coordinate of the cell in the map
            Returns:
                Point object representing the top left corner of the cell
        """
        return Point(x * Parameters.cell_size, y * Parameters.cell_size)

    def get_cell_position(self, point):
        """
            Args:
                point: Point object
            Returns:
                Tuple of cell position (x, y) of the given point
        """
        return (point.x // Parameters.cell_size, point.y // Parameters.cell_size) 
                    
        