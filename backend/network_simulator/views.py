from django.shortcuts import render
from django.http import HttpResponse
#from restframework import viewset

import sys
import os
sys.path.append("/".join([os.getcwd(), "network_simulator", "application_logic"]))

import network_simulation_entry_point as sim

network_routing_system = None

def init_sim(req, base_station_list):
    """
    Initializes the system and returns the graph as json. If it is called and
    the system is already initialized, then it will just return the json graph of the
    first initialization since the server was launched. To create a new graph altogether
    the server must be reset.
    """
    global network_routing_system
    if not network_routing_system:
        try:
            base_station_arr = [int(device) for device in base_station_list if device != "_"]
            network_routing_system = sim.NetworkSimulationEntryPoint(base_station_arr)
            json_graph = network_routing_system.retrieve_random_graph_as_json()
            return HttpResponse(json_graph, status=200)
        except ValueError as err: 
            return HttpResponse("Error: " + str(err), status=400)
    else:
        json_graph = network_routing_system.retrieve_random_graph_as_json()
        return HttpResponse(json_graph, status = 200)
    
def route_data(req, source, dest):
    """
    Query and retrieve the stats from the graph here
    """
    global network_routing_system
    if not network_routing_system:
        return HttpResponse("Error: Must initialize app before query", status=400)
    json_stats = network_routing_system.retrieve_query_results_as_json(source, dest)
    return HttpResponse(json_stats, status=200)
    
def collect_stats(req):
    """
    Retrieve all the system stats
    """
    global network_routing_system
    if not network_routing_system:
        return HttpResponse("Error: Must initialize app before query", status=400)
    json_stats = network_routing_system.retrieve_system_results_as_json()
    return HttpResponse(json_stats, status=200)
    return HttpResponse('collect stats')