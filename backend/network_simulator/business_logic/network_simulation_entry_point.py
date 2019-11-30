import grid
import graph

#class NetworkSimulationEntryPoint:
#    
#    def __init__(self, num_base_stations, num_devices):
#        = grid.Grid(3, 6)
#        main_graph = graph.RoutingSystemMasterGraph(main_grid)

if __name__ == "__main__":
    inp = [5,5,5,5,5]
    main_grid = grid.Grid(inp)
    print(main_grid)
    main_graph = graph.RoutingSystemMasterGraph(main_grid.device_data,
                                                main_grid.TRANSMISSION_RADIUS)
    print(main_graph)
    while True:
        x = input("Please specify query path")
        source, dest = x[:3], x[3:]
        print(source, dest)
        print(main_graph.query_for_optimal_route(source, dest))