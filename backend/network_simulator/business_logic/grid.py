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
    TRANSMISSION_RADIUS = 2
    
    def __init__(self, num_base_stations, num_devices):
        """
        Will Generate a grid of size 10 * 10 as an array of arrays
        """
        # TODO: Add decorator for input validation: 1 to 9 base stations and
        # base_stations to 20?? routable devices
        # TODO: Make sure that the global_id never reaches near 100. Make sure
        # to test on tons of values to see what
        # works consistently to define input bounds
        self.global_id_inc = 1
        self.grid = [[self.EMPTY_SPACE for _ in range(self.DIMENSIONS)] 
                      for _ in range(self.DIMENSIONS)]
        self.device_data = self._add_devices(num_base_stations, num_devices)
        
    def __repr__(self):
        repr_str = ""
        for row in self.grid:
            repr_str = repr_str + " ".join(row) + "\n"
        return repr_str
        
    def _scan_area_around_base_station_for_placement(self, x_coor, y_coor):
        """
        Scans the transmission self.TRANSMISSION_RADIUS make sure that the
        base stations are far enough apart.
        """
        # Board bounds can't be below 0
        check_and_fix_lower_bounds = lambda x: 0 if x < 0 else x 
        # Board bounds can't be below self.DIMENSIONS-1
        check_and_fix_upper_bounds = (lambda x:
                                      self.DIMENSIONS - 1
                                      if x > self.DIMENSIONS - 1
                                      else x)
        create_bounds = namedtuple("Bounds", "x0 x1 y0 y1")
        boundaries = create_bounds(check_and_fix_lower_bounds(y_coor -
                                    self.TRANSMISSION_RADIUS),
                                   check_and_fix_upper_bounds(y_coor +
                                    self.TRANSMISSION_RADIUS),
                                   check_and_fix_lower_bounds(x_coor -
                                    self.TRANSMISSION_RADIUS),
                                   check_and_fix_upper_bounds(x_coor +
                                    self.TRANSMISSION_RADIUS))
        for i in range(boundaries.x0, boundaries.x1 + 1):
            for j in range(boundaries.y0, boundaries.y1 + 1):
                if self.grid[j][i][0] == self.BASE_STATION_ROOT:
                    return False, boundaries
        return True, boundaries
        
    def _add_devices(self, num_base_stations, num_devices):
        """
        Adds all the user devices and base station devices to the grid and
        generates data structure (map[string]string) of base stations to 
        all there routable devices
        """
        # TODO: Refactor this line to work with all inputs
        devices_per_base_station = int(num_devices / num_base_stations)
        device_data = {}
        # Add in base stations
        for _ in range(num_base_stations):
            while True:
                
                x_coor = random.randint(1,10) - 1
                y_coor = random.randint(1, 10) - 1
                
                if self.grid[y_coor][x_coor] != self.EMPTY_SPACE:
                    continue
                
                is_space_free, base_station_boundaries = \
                self._scan_area_around_base_station_for_placement(y_coor, x_coor)
                
                if is_space_free:
                    curr_base_station = \
                        (self.BASE_STATION_ROOT + 
                        ("0" if 0 < self.global_id_inc < 10 else "") + 
                        str(self.global_id_inc))
                    self.grid[y_coor][x_coor] = curr_base_station
                    create_entry_for_base_station = namedtuple("BaseStationEntry", "base_station_coordinates routable_devices")
                    
                    device_data[curr_base_station] = create_entry_for_base_station((x_coor, y_coor), list())
                    self.global_id_inc += 1
                    
                    # For the transimssion radius of a base station,
                    # add its associated user devices
                    for _ in range(devices_per_base_station):
                        
                        while True:
                            
                            x_coor = random.randint(1,10) - 1
                            y_coor = random.randint(1, 10) - 1
                            
                            if (self.grid[y_coor][x_coor] == self.EMPTY_SPACE
                                and base_station_boundaries.x0 
                                    <= x_coor <= base_station_boundaries.x1
                                and base_station_boundaries.y0 
                                    <= y_coor <= base_station_boundaries.y1):
                                    curr_routable_device = \
                                        (self.ROUTABLE_DEVICE_ROOT + 
                                        ("0" if 0 < self.global_id_inc < 10 else "") + 
                                        str(self.global_id_inc))
                                    self.grid[y_coor][x_coor] = curr_routable_device
                                    create_routable_device_data = namedtuple("RoutableDevice", "routable_device_name coordinates")
                                    curr_device = create_routable_device_data(curr_routable_device, (x_coor, y_coor,))
                                    device_data[curr_base_station].routable_devices.append(curr_device)
                                    self.global_id_inc += 1
                                    break
                    break
        return device_data
            
if __name__ == "__main__":
    # TODO: As is we need to have the number of devices evenly divide the
    # number of base stations
    x = Grid(2, 4)
    print(x)
