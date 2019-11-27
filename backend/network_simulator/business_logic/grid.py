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
    BASE_STATION_TRANSMISSION_RADIUS = 2
    DEVICE_TRANSMISSION_RADIUS = 1
    
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
        def add_base_stations(how_many):
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
                
                # print("Starting new base station")
                for i in range(boundaries.y0, boundaries.y1 + 1):
                    for j in range(boundaries.x0, boundaries.x1 + 1):
                        if self.grid[j][i] != self.EMPTY_SPACE:
                            return False
                return True
                
#                print(boundaries)
#                boundary_0_0 = check_and_fix_lower_bounds(y_coor - radius), check_and_fix_lower_bounds(x_coor - radius)
#                boundary_X_0 = check_and_fix_upper_bounds(y_coor + radius), check_and_fix_lower_bounds(x_coor - radius)
#                boundary_0_Y = check_and_fix_lower_bounds(y_coor - radius), check_and_fix_upper_bounds(x_coor + radius)
#                boundary_X_Y = check_and_fix_upper_bounds(y_coor + radius), check_and_fix_upper_bounds(x_coor + radius)
##                for i in range(boundary0_0[0], boundary_X_0[0]):
##                    for j in range(boundary0_0[])
#                print(boundary_0_0)
#                print(boundary_X_0)
#                print(boundary_0_Y)
#                print(boundary_X_Y)
##                for i in range(boundary_0_0, boundary_X_0):
#                    for j in range(boundary_0_Y, boundary_X_Y):
#                        print(i, j)
                # return self.grid[x_coor][y_coor] == self.EMPTY_SPACE
            for _ in range(how_many):
                while True:
                    # *** Note about array indexing *** :
                    # With array indexing, the first index defines which array (y axis) and the second which 
                    # value in the array we use (x axis). So we need to reverse the indices when choosing values on grid.
                    # Also the array 0,0 is at the top left side of __repr__ grid and 9, 9 is bottom right of grid
                    # The create_bounds namedtuple will treat the x coordinate and y coordinate as we would intuitively expect
                    x_coor = random.randint(1,10) - 1
                    y_coor = random.randint(1, 10) - 1
                    if scan_for_free_space(y_coor, x_coor, self.BASE_STATION_TRANSMISSION_RADIUS):
                        self.grid[y_coor][x_coor] = (self.BASE_STATION_ROOT + 
                                                     ("0" if 0 < self.global_id_inc < 10 else "") + 
                                                     str(self.global_id_inc))
                        self.global_id_inc += 1
                        break
        add_base_stations(num_base_stations)
#        def find_free_space_and_add(device_name, how_many):
#            for _ in range(how_many):
#                while True:
#                    x_coor = random.randint(1,10) - 1
#                    y_coor = random.randint(1, 10) - 1
#                    if self.grid[x_coor][y_coor] == self.EMPTY_SPACE:
#                        self.grid[x_coor][y_coor] = (device_name + 
#                                                     ("0" if 0 < self.global_id_inc < 10 else "") + 
#                                                     str(self.global_id_inc))
#                        self.global_id_inc += 1
#                        break
#        find_free_space_and_add(self.BASE_STATION_ROOT, num_base_stations)
        #find_free_space_and_add(self.ROUTABLE_DEVICE_ROOT, num_devices)
        
                    
                    
                
            
    
#    def __init__(self, num_base_stations, num_devices):
#        self.grid = [[None for _ in range(self.DIMENSIONS)] for _ in range(self.DIMENSIONS)]
#        self.base_stations = []
#        self.user_devices = []
#        self.coordinates_map = {}
#        self.graph = nx.Graph()
#        self.init_random(num_base_stations, num_devices)
#        
#    def show_grid(self):
#        def transform_list(arr):
#            output_arr = []
#            for _, elem in enumerate(arr):
#                if elem == None:
#                    output_arr.append(" -- ")
#                elif elem == ",":
#                    output_arr.append("")
#                elif elem == "[":
#                    output_arr.append("|")
#                elif elem == "]":
#                    output_arr.append("|")
#            print("".join(output_arr))
#        
#        for row in self.grid:
#            transform_list(row)
#            
#            
#    def select_channel(self):
#        return random.randint(1, self.NUM_CHANNELS)
#        
#                

#        
#    def init_random(self, num_base_stations, num_devices):
#        possibleCoordinates = []
#        
#        #Partition graph into regions by x coordinate
#        region_size = math.ceil(self.DIMENSIONS / num_base_stations)
#        print(region_size)
#        num_of_regions = math.ceil(self.DIMENSIONS / region_size)
#        print(num_of_regions)
#        
#        for i in range(self.DIMENSIONS):
#            for j in range(self.DIMENSIONS):
#                possibleCoordinates.append([j, i])
#                
#        max_index = self.DIMENSIONS ** 2
#        
#        regions = [0 for _ in range(region_size)]
#        regions = []
#        
#        for i in range(num_of_regions):
#            fromm = region_size * i * self.DIMENSIONS
#            to = fromm + region_size * self.DIMENSIONS
#            if to > max_index:
#                to = max_index
#            to = to - 1
#            region = possibleCoordinates[fromm:to]
#            random.shuffle(region)
#            regions.append(region)
#            
#        base_station_coordinates = []
#        
#        for i in range(num_base_stations):
#            region = regions[i%num_of_regions]
#            coordinates = region[0]
#            del region[0]
#            base_station_coordinates.append(coordinates)
#            base_station_id = "b"+str(i)
#            self.grid[coordinates[0]][coordinates[1]] = base_station.BaseStation(base_station_id)
#            self.coordinates_map[base_station_id] = coordinates
#            self.base_stations.append(base_station_id)
#            
#        
#            
            
if __name__ == "__main__":
    x = Grid(3, 10)
    print(x)
