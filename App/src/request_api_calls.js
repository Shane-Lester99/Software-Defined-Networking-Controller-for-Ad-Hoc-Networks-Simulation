/*
This module will be used to call the Python/django backend REST interface
*/
const fetch = require("node-fetch")


/*
async await functions. Don't call these directly, I have built wrappers around
them that will take away aysnchronous bugs for the frontend developers
*/

async function callInitSystem(baseStationArray) {
   
    console.log("Init system with ", baseStationArray);
    const bsString = baseStationArray.join("_");
    const url = "http://127.0.0.1:8080/network_simulator/init_sim/" + bsString
    const res = await fetch(url)
        .then(res => res.json())
        .then(json_random_graph => {
            return json_random_graph
        }).catch(err => err)
    return res
}

function callQueryRoute(source, dest) {
    console.log("Call query route with", source, dest)
    return
}

function callSystemStats() {
    console.log("Call get all system stats")
    return
}

module.exports = {
    "callInitSystem": callInitSystem
}

// randomGraph = callInitSystem([1,3,3,4])
// setTimeout(function(rg){console.log(rg)}, 10, randomGraph)

//callQueryRoute("R02", "R03")
//callSystemStats()