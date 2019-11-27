from networkx import nx
import math
import random

class Grid:
    
    DIMENSIONS = 10
    NUM_CHANNELS = 5
    
    def __init__(self, num_base_stations, num_devices):
        self.grid = [[None for _ in range(self.DIMENSIONS)] for _ in range(self.DIMENSIONS)]
        self.baseStations = []
        self.userDevices = []
        self.coordinatesMap = {}
        self.graph = nx.Graph()
        #self.init_random(num_base_stations, num_devices)
        
    def show_grid(self):
        def transform_list(arr):
            output_arr = []
            for _, elem in enumerate(arr):
                if elem == None:
                    output_arr.append(" -- ")
                elif elem == ",":
                    output_arr.append("")
                elif elem == "[":
                    output_arr.append("|")
                elif elem == "]":
                    output_arr.append("|")
            print("".join(output_arr))
            
        for row in self.grid:
            transform_list(row)
                

if __name__ == "__main__":
    x = Grid(3, 10)
    x.show_grid()
        
#    def init_random(self, num_base_stations, num_devices):
#        possibleCoordinates = []
#        
#        # Partition graph into regions by x coordinate
#        region_size = math.ceil(self.DIMENSIONS / num_base_stations)
#        num_of_regions = math.ceil(self.DIMENSIONS / region_size)
#        
#        for i in range(self.DIMENSIONS):
#            for j in range(self.DIMENSIONS):
#                possibleCoordinates.append([j, i])
#                
#        max_index = self.DIMENSIONS ** 2
#        
#        #regions = [0 for _ in range(region_size)]
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
#            coordinate = region[0]
#            del region[0]
#            base_station_coordinates.append(coordinates)
#            base_station_id = "b"+i
#            self.grid[coor]