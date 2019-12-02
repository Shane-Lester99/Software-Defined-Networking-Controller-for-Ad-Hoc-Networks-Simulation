/*
This module will be used to call the Python/django backend REST interface

To see how the JSON is formatted, go to 
backend.network_simulator.application_logic.network_simulation_entry_point.py
and read the comments above the API calls
*/
const fetch = require("node-fetch")

// baseURL is for localhost for demo, this will be deleted if this app
// is used past demos.
const baseUrl = "http://127.0.0.1:8080/network_simulator"

// Note: Make sure to call this function to init the system before calling
// the two below
async function callInitSystem(baseStationArray) {
    const bsString = "/init_sim/" + baseStationArray.join("_");
    const url = baseUrl + bsString
    const res = await fetch(url)
        .then(res => res.json())
        .then(json_random_graph => json_random_graph)
        .catch(err => err)
    return res
}


async function callQueryRoute(source, dest) {
    const url = baseUrl + "/route_data/" + source + "/" + dest
    const res = await fetch(url)
        .then(res => res.json())
        .then(json_stats => json_stats)
        .catch(err => err)
    return res
}

async function callSystemStats() {
    const url = baseUrl + "/collect_stats/"
    const res = await fetch(url)
    .then(res => res.json())
    .then(json_stats => json_stats)
    .catch(err => err)
    return res
}


// This is an example of how to call these async functions. Note that 
// callInitSystem is what has to be called first (or else 400 response). 
// After it is called if it is called again it won't reinit the graph, 
// it will instead return the same json graph.

// Also note that the django sever must be launches with ./run_backend.sh before
// we call the API on path network-routing-simulation.backend.run_backend.sh

/*
const initSim = callInitSystem([4,4,4])
initSim.then(x => console.log("graphinit ", x))
       .then(function() {
            const query = callQueryRoute("R02", "R03")
            query.then(x => console.log("Query1", x))
            .catch(err => console.log(err))
        })
        .then(function() {
            const query = callQueryRoute("R02", "R04")
            query.then(x => console.log("Query2", x))
            .catch(err => console.log(err))
        })
        .then(function() {
            const outputStats = callSystemStats()
            outputStats.then(x => console.log("sys stats", x))
            .catch(err => console.log(err))
        })
        .catch(err => err)
 */      