import random
from collections import namedtuple
from decorators import validate_grid_input

class Grid:
    
    DIMENSIONS = 10
    EMPTY_SPACE = "___"
    BASE_STATION_ROOT = "B"
    ROUTABLE_DEVICE_ROOT = "R"
    TRANSMISSION_RADIUS = 2
    
    @validate_grid_input
    def __init__(self, base_station_list):
        """
        Will Generate a grid of size 10 * 10 as an array of arrays
        """
        self.global_id_inc = 1
        self.grid = [[self.EMPTY_SPACE for _ in range(self.DIMENSIONS)] 
                      for _ in range(self.DIMENSIONS)]
        self.device_data = self._add_devices(base_station_list)
        
    def __repr__(self):
        repr_str = "***Grid of Network Routing System***\n"
        for row in self.grid:
            repr_str = repr_str + " ".join(row) + "\n"
        return repr_str
        
    def _add_devices(self, base_station_list):
        """
        Adds all the user devices and base station devices to the grid and
        generates data structure (map[string]string) of base stations to 
        all there routable devices
        """
        device_data = {}
        for bs_index in range(len(base_station_list)):
            while True:
                
                x_coor = random.randint(1,10) - 1
                y_coor = random.randint(1, 10) - 1
                
                if self.grid[y_coor][x_coor] != self.EMPTY_SPACE:
                    continue
                
                is_space_free, base_station_boundaries = \
                self._scan_area_around_base_station_for_placement(y_coor, x_coor)
                
                if is_space_free:
                    curr_base_station = self._create_label(self.BASE_STATION_ROOT)
                    self.grid[y_coor][x_coor] = curr_base_station
                    create_entry_for_base_station = \
                                    namedtuple("BaseStationEntry",
                                    "base_station_coordinates routable_devices")
                    
                    device_data[curr_base_station] = \
                        create_entry_for_base_station((x_coor, y_coor), list())
                    for _ in range(base_station_list[bs_index]):
                        
                        while True:
                            
                            x_coor = random.randint(1,10) - 1
                            y_coor = random.randint(1, 10) - 1
                            
                            if (self.grid[y_coor][x_coor] == self.EMPTY_SPACE
                                and base_station_boundaries.x0 
                                    <= x_coor <= base_station_boundaries.x1
                                and base_station_boundaries.y0 
                                    <= y_coor <= base_station_boundaries.y1):
                                    curr_routable_device = self._create_label(self.ROUTABLE_DEVICE_ROOT)
                                    self.grid[y_coor][x_coor] = curr_routable_device
                                    create_routable_device_data = namedtuple("RoutableDevice",
                                            "routable_device_name coordinates")
                                    curr_device = \
                                        create_routable_device_data(curr_routable_device,
                                                                   (x_coor, y_coor,))
                                    device_data[curr_base_station].routable_devices.append(curr_device)
                                    break
                    break
        return device_data
    
    def _create_label(self, label_type):
        """
        Creates the label for a base station or a routable user device in the
        grid
        """
        def create_new_global_id():
            new_global_id = self.global_id_inc
            if new_global_id >= self.DIMENSIONS * self.DIMENSIONS:
                raise ValueError
            self.global_id_inc += 1
            return new_global_id
            
        global_id = create_new_global_id()
        return (label_type + ("0" if 0 < global_id < 10 else "") + str(global_id))
        
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