import grid
import graph

class NetworkSimulationEntryPoint:
    
    def __init__(self, base_station_list):
        self._entry_grid = grid.Grid(base_station_list)
        self._entry_graph = graph.RoutingSystemMasterGraph(
            self._entry_grid.device_data,
            self._entry_grid.TRANSMISSION_RADIUS)
            
    def command_line_test_exp(self):
        """
        this will allow the user to run a test without the use of the API
        """
        print(self._entry_grid)
        print(self._entry_graph)
        while True:
            exit_string = input("Would you like to specify a query path (Y/N):")
            if exit_string == "N" or exit_string == "n":
                print(self._entry_graph.output_system_stats())
                break
            x = input("Please specify query path in form <device_id_1><device_id2>:")
            source, dest = x[:3], x[3:]
            print(self._entry_graph.query_for_optimal_route(source, dest))

if __name__ == "__main__":
    bs_list = [5 for _ in range(9)]
    entry = NetworkSimulationEntryPoint(bs_list)
    entry.command_line_test_exp()
