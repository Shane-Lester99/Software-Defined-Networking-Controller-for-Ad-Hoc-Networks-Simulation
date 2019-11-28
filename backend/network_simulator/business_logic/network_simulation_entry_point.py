import grid
import graph

#class NetworkSimulationEntryPoint:
#    
#    def __init__(self, num_base_stations, num_devices):
#        = grid.Grid(3, 6)
#        main_graph = graph.RoutingSystemMasterGraph(main_grid)

if __name__ == "__main__":
    main_grid = grid.Grid(4,16)
    print(main_grid)
    main_graph = graph.RoutingSystemMasterGraph(main_grid.device_data,
                                                main_grid.TRANSMISSION_RADIUS)
    print(main_graph)