import React from 'react';
import './styles/index.css';
import data from '../../assets/data.json';
import channel from '../../assets/channel.json';

class LandingPage extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
      numberOfNodes: "",
      numberOfBaseStations: 0,
      channel: 5,
      elements: [],
      displayError: "hidden",
    };
    this.randomize = this.randomize.bind(this);
    this.getRandomInt = this.getRandomInt.bind(this);
    this.nodeInput = this.nodeInput.bind(this);
    this.baseStationInput = this.baseStationInput.bind(this);
  }

  getRandomInt (max) {
    return Math.floor(Math.random() * Math.floor(max));
  }

  randomize () {
    let nodes = this.state.numberOfNodes.split(',');
    let incorrectInput = nodes.length !== this.state.numberOfBaseStations ||
      nodes.some(node => {
        return isNaN(node);
      });

    if(incorrectInput || isNaN(this.state.channel) ||
      isNaN(this.state.numberOfBaseStations) ||
      this.state.numberOfBaseStations < 1 || 
      this.state.numberOfBaseStations > 3 ||
      this.state.channel < 4 ||
      this.state.channel > 10) {
      
        this.setState({displayError: "show"});
        return;
    } else {
      this.setState({displayError: "hidden"})
    }

    console.log(nodes.map(num => parseInt(num)));

    let graph = [];
    for(const node in data) {
      let device = {
        data: {
          id: node,
          label: node,
          type:'device',
          base_station_name: data[node].metadata.base_station_name,
        },
        position: {
          x:data[node].metadata.node_coordinates[0]*10,
          y:data[node].metadata.node_coordinates[1]*10,
        }
      }
      graph.push(device);

      /*
      for(const edges in data[node].edges) {

        let edge = {
          data: {
            source: node,
            target: data[node].edges[edges],
            label: `10`,
            color: "red",
            type: "edge",
          },
          group:"edges"
        }
        graph.push(edge);
      }
      */
    }
    /*
    for (let num = 0; num < this.state.numberOfNodes; num++) {
      let data = {
        data: {
          id: num,
          label: `N${num}`,
          type:'device'
        },
        position: {
          x: this.getRandomInt(100),
          y: this.getRandomInt(100)
        },
      };
      elements.push(data);
    }
    for (let num = 0; num < this.state.numberOfBaseStations; num++) {
      let data = {
        data: {
          id: `Base Station ${num}`,
          label: `BS${num}`,
          type: 'baseStation'
        },
        position: {
          x: this.getRandomInt(100),
          y: this.getRandomInt(100)
        }
      };
      elements.push(data);
    }
    
    for (let num = 0; num <= this.state.numberOfNodes; num++) {
      let source = this.getRandomInt(this.state.numberOfNodes);
      let target = this.getRandomInt(this.state.numberOfNodes);
      if(source != target) {
        let data = {
          data: {
            source: source,
            target: target,
            label: `Edge from ${source} to ${target}`
          }
        };
        elements.push(data);
      }
    }
    */

    this.props.setData(graph,channel);
    this.props.changePage("Graph");
  }

  nodeInput = (e) => {
      this.setState({
        numberOfNodes: e.target.value,
      })
  }

  channelInput = (e) => {
    this.setState({
      channel: parseInt(e.target.value),
    })
}

  baseStationInput = (e) => {
      this.setState({
        numberOfBaseStations: parseInt(e.target.value)
      })
  }

  render() {
    return(
      <div id="landingPage">
        <h1 id="title">Wireless Network Simulation </h1>
        <div id="prompt">
          <h2>Please Enter </h2>
          {
            <p id="errorMessage" className={this.state.displayError}>
              Invalid Input
            </p> 
          }
          <h3>Number of Nodes Per Base Station</h3>
          <input placeholder={'Comma separated'} onChange={this.nodeInput} />
          <br/>
          <h3>Number of Channels</h3>
          <input placeholder={'4-10'} onChange={this.channelInput} />
          <br/>
          <h3>Number of Base Stations</h3>
          <input placeholder={'1-3'} onChange={this.baseStationInput}/>
          <br/>
          <button id="randomizeButton" onClick={this.randomize}>Randomize</button>
        </div>
      </div>
    )
  }
}

export default LandingPage;