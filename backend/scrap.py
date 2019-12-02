import sys
import os
sys.path.append('/'.join([os.getcwd(),'network_simulator', 'application_logic']))
import network_simulation_entry_point
x = network_simulation_entry_point.NetworkSimulationEntryPoint([1,2,2])
print(x.retrieve_random_graph_as_json())