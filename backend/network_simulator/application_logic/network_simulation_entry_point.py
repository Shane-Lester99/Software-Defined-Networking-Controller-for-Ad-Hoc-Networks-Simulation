import grid
import graph

class NetworkSimulationEntryPoint:
    """
    Entry point of NetworkSimulation application. It provides an 
    interface over the application modules and returns the results as JSON.
    It also allows for backend debugging with a CLI version of the application.
    
    To run the CLI version run the module from the main function
    """
    
    def __init__(self, base_station_list):
        self._entry_grid = grid.Grid(base_station_list)
        self._entry_graph = graph.RoutingSystemMasterGraph(
            self._entry_grid.device_data,
            self._entry_grid.TRANSMISSION_RADIUS)
            
    def command_line_test_exp(self):
        """
        This will allow the user to run a test without the use of the API. 
        THe user can write queries on the command line and once they exit they
        will retrieve the system output stats. The purpose of this function is
        for backend debugging.
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
            
    def retrieve_random_graph_as_json(self):
        """
        For the initialization function call of the API. This function will return
        the random graph that will remain static after initialization.
        """
        return
    
    def retrieve_query_results_as_json(self, source_node, dest_node):
        """
        The API allows for running a single query, and this will be the output.
        """
        return
    
    def retrieve_system_results_as_json(self):
        """
        The API allows for seeing all the results of all the queries.
        """
        return
    
    

if __name__ == "__main__":
    # This will run a test so that the user can query from the command line to
    # debug the backend
    print("This is the CLI version of the Network Routing Simulation.")
    print("To set up the network topology, write a list of 1 to 9 numbers.")
    print("Each number signifies how many user devices are associated with that base station.\n")
    x = input("Please enter these numbers now as a single space seperated list:")
    bs_list = [int(char) for char in x if char != " "]
    entry = NetworkSimulationEntryPoint(bs_list)
    entry.command_line_test_exp()
