from networkx import nx
import math
import random
import base_station
from collections import namedtuple

class Grid:
    
    DIMENSIONS = 10
    NUM_CHANNELS = 5
    EMPTY_SPACE = "___"
    BASE_STATION_ROOT = "B"
    ROUTABLE_DEVICE_ROOT = "R"
    NON_ROUTABLE_DEVICE_ROOT = "H"
    TRANSMISSION_RADIUS = 2
    
    def __init__(self, num_base_stations, num_devices):
        """
        Will Generate a grid of size 10 * 10 as an array of arrays
        """
        # TODO: Add decorator for input validation: 1 to 5 base stations and 1-10 routable devices
        self.global_id_inc = 1
        self.grid = [[self.EMPTY_SPACE for _ in range(self.DIMENSIONS)] for _ in range(self.DIMENSIONS)]
        self._add_devices(num_base_stations, num_devices)
        
    def __repr__(self):
        repr_str = ""
        for row in self.grid:
            repr_str = repr_str + " ".join(row) + "\n"
        return repr_str
        
    def _add_devices(self, num_base_stations, num_devices):
        """
        Adds all the user devices and base station devices to the grid
        """
        # *** Note about array indexing *** :
        # With array indexing, the first index defines which array (y axis) and the second which 
        # value in the array we use (x axis). So we need to reverse the indices when choosing values on grid.
        # Also the array 0,0 is at the top left side of __repr__ grid and 9, 9 is bottom right of grid
        # The create_bounds namedtuple will treat the x coordinate and y coordinate as we would intuitively expect
        def scan_for_free_space(x_coor, y_coor, radius):
            """
            Scans the transmission radius self.BASE_STATION_TRANSMISSION_RADIUS to
            make sure that the base stations are far enough apart
            """
            # Board bounds can't be below 0
            check_and_fix_lower_bounds = lambda x: 0 if x < 0 else x 
            # Board bounds can't be below self.DIMENSIONS-1
            check_and_fix_upper_bounds = lambda x: self.DIMENSIONS - 1 if x > self.DIMENSIONS - 1 else x
            create_bounds = namedtuple("bounds", "y0 y1 x0 x1")
            boundaries = create_bounds(check_and_fix_lower_bounds(y_coor - radius),
                                       check_and_fix_upper_bounds(y_coor + radius),
                                       check_and_fix_lower_bounds(x_coor - radius),
                                       check_and_fix_upper_bounds(x_coor + radius))
            for i in range(boundaries.y0, boundaries.y1 + 1):
                for j in range(boundaries.x0, boundaries.x1 + 1):
                    if self.grid[j][i] != self.EMPTY_SPACE:
                        return False
            return True
        for _ in range(num_base_stations):
            while True:
                x_coor = random.randint(1,10) - 1
                y_coor = random.randint(1, 10) - 1
                if scan_for_free_space(y_coor, x_coor, self.TRANSMISSION_RADIUS):
                    self.grid[y_coor][x_coor] = (self.BASE_STATION_ROOT + 
                                                 ("0" if 0 < self.global_id_inc < 10 else "") + 
                                                 str(self.global_id_inc))
                    self.global_id_inc += 1
                    break
            
            
if __name__ == "__main__":
    x = Grid(6, 10)
    print(x)
