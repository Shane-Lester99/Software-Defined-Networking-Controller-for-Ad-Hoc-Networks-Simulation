import React from 'react';
import CytoscapeComponent from "react-cytoscapejs";
import Icon from '../../assets/touch-screen.svg';
import './styles/index.css'
import StatPage from './StatsPage';

export default class GraphPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      source: '',
      target: '',
      type:'',
      name: '',
      baseStation: '',
      reachableNodes: [],
      x: '',
      y: '',
      queryNumber: 0,
      label: '',
    }
    this.addLink = this.addLink.bind(this);
    this.sourceInput = this.sourceInput.bind(this);
    this.targetInput = this.targetInput.bind(this);
    this.channelData = this.channelData.bind(this);
    this.getColor = this.getColor.bind(this);
  }

  async componentDidMount() {
    if(this.state.tab === "stats")
      return;
    this.cy.center();
    this.cy.nodes().ungrabify();
    this.cy.on('click', 'node[type="device"]', async function(evt){
      let node = evt.target;
      let id = node.id();
      let position = node.position();
      
      let reachableNodes = await fetch(`http://127.0.0.1:8080/network_simulator/get_reachable_nodes/${id}`)
      .then(res => res.json())
      .then(data => data);

      this.setState({
        type:'Device',
        name: `Node ${id}`,
        x:position.x/10,
        y:position.y/10,
        baseStation: node._private.data.base_station_name,
        reachableNodes: reachableNodes,
      })
    }.bind(this));
    this.cy.on('click', 'node[type="baseStation"]', function(evt){
      let node = evt.target;
      let id = node.id();
      let position = node.position();
      this.setState({
        type:'Base Station',
        name: id,
        x:position.x/10,
        y:position.y/10,
      })
    }.bind(this));
    this.cy.on('click', 'edge', function(evt){
      let edge = evt.target;
      let source = edge.data('source');
      let target = edge.data('target');
      let label = edge.data('label');
      let channel = edge.data('channel');
      this.setState({
        type:'Edge',
        name: `Edge from Node ${source} to Node ${target}`,
        channel: channel,
        label: label,
      })
    }.bind(this));
  }

  channelData = () => {
    
    let channels = this.props.channel.map((cost,index) => {
      return <tr key={index} style={{backgroundColor:this.getColor(index)}}>
        <td>{index}</td>
        <td>{cost}</td>
      </tr>
    })
    return <table id="table">
    <thead>
    <tr>
        <th key="channel">Channel</th>
        <th key="cost">Cost</th>
    </tr>
    </thead>
    <tbody>
      {channels}
    </tbody>
</table>
  }

  addLink = async() => {
    let routeData = await fetch(`http://127.0.0.1:8080/network_simulator/route_data/${this.state.source}/${this.state.target}`)
    .then(res => res.json())
    .then(data => data)
    .catch(err => err);
    try {
      if (Object.entries(routeData).length === 0 && routeData.constructor === Object)
        throw "Path Could not be established"
      let current;
      let previous;
      for(const route in routeData) {
        if(current === undefined) {
          current = route;
        } else {
          previous = current;
          current = route;
          let edge= {
            group: "edges",
            data: {
              source: previous,
              target: current,
              channel: routeData[route][0],
              label: this.state.queryNumber, 
              color: this.getColor(routeData[route][0]),
            }
          }
          this.cy.add(edge);
        }
      }
    }
    catch {
      alert('Path could not be established');
      return;
    }
    this.setState({queryNumber: this.state.queryNumber+1});
  }

  getColor = (channel) => {
    let colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', 
    '#f032e6', '#bcf60c', '#fabebe'];
    return colors[channel];
  }

  sourceInput = (e) => {
      this.setState({
        source: e.target.value,
      })
  }

  targetInput = (e) => {
      this.setState({
        target: e.target.value,
      })
  }

  getText = () => {
    let text = "";
    this.state.reachableNodes.sort().forEach((device,index) => {
      if(index === 0) {
        text += device;
      } else {
        text += ', ' + device;
      }
    })
    return text;
  }

  getData = () => {
    if(this.state.type === 'Device')
      return (
        <div id="informationBox">
          <p>Type: {this.state.type}</p>
          <p>Label: {this.state.name}</p>
          <p>Base Station: {this.state.baseStation}</p>
          <p>Reachable Nodes: {this.getText()}</p>
          <p>Coordinates: {`[${this.state.x}, ${this.state.y}]`}</p>
        </div>  
      )
    else if(this.state.type === 'Base Station')
      return (
        <div id="informationBox">
          <p>Type: {this.state.type}</p>
          <p>Label: {this.state.name}</p>
          <p>Coordinates: {`[${this.state.x}, ${this.state.y}]`}</p>
        </div>  
      )
    else if(this.state.type === 'Edge')
      return (
        <div id="informationBox">
          <p>Type: {this.state.type}</p>
          <p>Label: {this.state.name}</p>
          <p>Channel: {`${this.state.channel}`}</p>
          <p>Query Number: {`${this.state.label}`}</p>
        </div> 
      )
  }

  reset = async() => {
    await fetch("http://127.0.0.1:8080/network_simulator/reset/")
    .then(res => res)
    .catch(err => err)
    this.props.changePage('Landing');
  }

  render () {
    return (
      <div id="graphPage">
        <h1 id="graphTitle">Network Simulation</h1>
        <div id="graphContainer">
          <div id="channel">
            {this.channelData()}
          </div>
            <CytoscapeComponent
              className={"graph"}
              cy={(cy) => { this.cy = cy }}
              elements={this.props.data}
              zoom={5}
              stylesheet={stylesheet}
            />
            <div id="data">
              <div id="addLink">
                <h2>Add Connection</h2>
                <input placeholder={"Source Node"} onChange={this.sourceInput}></input>
                <input placeholder={"Target Node"} onChange={this.targetInput}></input>
                <br/>
                <button id="addButton" onClick={this.addLink}>Add Route</button>
              </div>
              <h2 style={{textAlign:'center'}}>Selected Data</h2>
              {this.getData()}
              <button id="resetButton" onClick={this.reset}>Reset</button>
            </div>
        </div>
      </div>
    );
  }
}

const stylesheet = [
  {
    selector: 'node[type="device"]',
    style: {
      width: 6,
      height: 8,
      shape: 'rectangle',
      backgroundImage: Icon,
      backgroundFit: 'contain',
      label: 'data(label)',
      fontSize: 2,
      backgroundOpacity: 0,
    }
  },
  {
    selector: 'node[type="baseStation"]',
    style: {
      width: 4,
      height: 4,
      shape: 'triangle',
      backgroundColor: 'orange',
      label: 'data(label)',
      fontSize: 3,
    }
  },
  {
    selector: 'edge',
    style: {
      width: 0.5,
      curveStyle:'bezier',
      targetArrowShape: 'triangle',
      arrowScale: 0.3,
      label: 'data(label)',
      lineColor: 'rgba(0, 0, 0, 0.5)',
      lineStyle: 'dotted',
      targetArrowColor: 'data(color)',
      fontSize:3,
      textMarginY: -3,
      textMarginX: 2,
    }
  }
]

