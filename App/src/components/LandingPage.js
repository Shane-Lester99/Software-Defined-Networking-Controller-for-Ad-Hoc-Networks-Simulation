import React from 'react';
import './styles/index.css';
import StatPage from './StatsPage';

class LandingPage extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
      numberOfNodes: "",
      tab: 'Home',
      channel: 0,
      elements: [],
      displayError: "hidden",
    };
    this.randomize = this.randomize.bind(this);
    this.getRandomInt = this.getRandomInt.bind(this);
    this.nodeInput = this.nodeInput.bind(this);
  }

  getRandomInt (max) {
    return Math.floor(Math.random() * Math.floor(max));
  }

  getGraph = async() => {
    let graph = await fetch(`http://127.0.0.1:8080/network_simulator/init_sim/${this.state.numberOfNodes}/${this.state.channel}`)
    .then(res => res.json())
    .then(random_graph => random_graph)
    .catch(err => err)
    return graph;
  }

  randomize = async() => {
    let nodes = this.state.numberOfNodes.split(',');
    let incorrectInput = !this.state.numberOfNodes || nodes.length > 8 ||
      nodes.some(node => {
        return isNaN(node) || parseInt(node) < 1 || parseInt(node) > 5;
      });

    if(incorrectInput || isNaN(this.state.channel) ||
      this.state.channel < 4 ||
      this.state.channel > 10) {
      
        this.setState({displayError: "show"});
        return;
    } else {
      this.setState({displayError: "hidden"})
    }

    const raw_graph = await this.getGraph();
    const data = raw_graph.graph;
    const channel = raw_graph.channels;
    let graph = [];
    let baseStations = [];
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
      if(baseStations.find(names => names === data[node].metadata.base_station_name) === undefined) {
        let bStation = {
          data: {
            id: data[node].metadata.base_station_name,
            label: data[node].metadata.base_station_name,
            type: 'baseStation',
          },
          position: {
            x:data[node].metadata.base_station_coordinates[0]*10,
            y:data[node].metadata.base_station_coordinates[1]*10,
          }
        }
        graph.push(bStation);
        baseStations.push(data[node].metadata.base_station_name);
      }
      graph.push(device);
    }

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

  changeTab = (e) => {
    this.setState({tab: e.target.getAttribute('name')})
  }

  tabBar = () => {
    if(this.state.tab === "Home") {
      return <div id="tabBar">
          <h2 className={`tab display`}>Home</h2>
          <h2 name="stats" className="tab" onClick={this.changeTab}>System Stats</h2>
        </div>
    } else if(this.state.tab === "stats") {
      return <div id="tabBar">
          <h2 name="Home" className={`tab`} onClick={this.changeTab}>Home</h2>
          <h2 className="tab display">System Stats</h2>
        </div>
    }
  }

  renderPage = () => {
    if(this.state.tab === "Home")
      return(
        <div id="prompt">
          <h2>Please Enter </h2>
          {
            <p id="errorMessage" className={this.state.displayError}>
              Invalid Input
            </p> 
          }
          <h3>Number of Nodes Per Base Station</h3>
          <input placeholder={'Comma separated (1-5)'} onChange={this.nodeInput} />
          <br/>
          <h3>Number of Channels</h3>
          <input placeholder={'4-10'} onChange={this.channelInput} />
          <br/>
          <br/>
          <button id="randomizeButton" onClick={this.randomize}>Randomize</button>
        </div>
      )
    else if(this.state.tab === "stats") {
      return <StatPage />
    }
  }

  render() {
    return(
      <div id="landingPage">
        <h1 id="title">Wireless Network Simulation </h1>
        {this.tabBar()}
        {this.renderPage()}
      </div>
    )
  }
}

export default LandingPage;