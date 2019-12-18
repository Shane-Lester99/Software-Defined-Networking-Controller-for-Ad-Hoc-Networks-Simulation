import React from 'react';
import CytoscapeComponent from "react-cytoscapejs";
import Icon from '../../assets/touch-screen.svg';
import routeData from '../../assets/route.json';
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
      x: '',
      y: '',
      tab: 'graph'
    }
    this.addLink = this.addLink.bind(this);
    this.sourceInput = this.sourceInput.bind(this);
    this.targetInput = this.targetInput.bind(this);
    this.channelData = this.channelData.bind(this);
    this.getRandomColor = this.getRandomColor.bind(this);
  }

  componentDidMount() {
    if(this.state.tab === "stats")
      return;
    this.cy.center();
    this.cy.nodes().ungrabify();
    this.cy.on('click', 'node[type="device"]', function(evt){
      let node = evt.target;
      let id = node.id();
      let position = node.position();
      this.setState({
        type:'Device',
        name: `Node ${id}`,
        x:position.x/10,
        y:position.y/10,
        baseStation: node._private.data.base_station_name,
      })
    }.bind(this));
    this.cy.on('click', 'node[type="baseStation"]', function(evt){
      let node = evt.target;
      let id = node.id();
      let position = node.position();
      this.setState({
        type:'Base Station',
        name: id,
        x:position.x,
        y:position.y,
      })
    }.bind(this));
    this.cy.on('click', 'edge', function(evt){
      let edge = evt.target;
      let source = edge.data('source');
      let target = edge.data('target');
      let label = edge.data('label');
      this.setState({
        type:'Edge',
        name: `Edge from Node ${source} to Node ${target}`,
        channel: label,
      })
    }.bind(this));
  }

  componentDidUpdate() {
    if(this.state.tab === "stats")
      return;
    this.cy.center();
    this.cy.nodes().ungrabify();
    this.cy.on('click', 'node[type="device"]', function(evt){
      let node = evt.target;
      let id = node.id();
      let position = node.position();
      this.setState({
        type:'Device',
        name: `Node ${id}`,
        x:position.x/10,
        y:position.y/10,
        baseStation: node._private.data.base_station_name,
      })
    }.bind(this));
    this.cy.on('click', 'node[type="baseStation"]', function(evt){
      let node = evt.target;
      let id = node.id();
      let position = node.position();
      this.setState({
        type:'Base Station',
        name: id,
        x:position.x,
        y:position.y,
      })
    }.bind(this));
    this.cy.on('click', 'edge', function(evt){
      let edge = evt.target;
      let source = edge.data('source');
      let target = edge.data('target');
      let label = edge.data('label');
      this.setState({
        type:'Edge',
        name: `Edge from Node ${source} to Node ${target}`,
        channel: label,
      })
    }.bind(this));
  }

  channelData = () => {
    
    let channels = this.props.channel.map((cost,index) => {
      return <tr key={index}>
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

  addLink = () => {

    try {
      let current;
      let previous;
      let color = this.getRandomColor();
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
              label: routeData[route][0],
              color: color,
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
  }

  getRandomColor = () => {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  sourceInput = (e) => {
    if(!isNaN(e.target.value) && parseInt(e.target.value) <= 10 && parseInt(e.target.value) >= 0)
      this.setState({
        source: e.target.value,
      })
  }

  targetInput = (e) => {
    if(!isNaN(e.target.value) && parseInt(e.target.value) <= 10 && parseInt(e.target.value) >= 0)
      this.setState({
        target: e.target.value,
      })
  }

  getData = () => {
    if(this.state.type === 'Device' || this.state.type === 'Base Station')
      return (
        <div id="informationBox">
          <p>Type: {this.state.type}</p>
          <p>Label: {this.state.name}</p>
          <p>Base Station: {this.state.baseStation}</p>
          <p>Coordinates: {`[${this.state.x}, ${this.state.y}]`}</p>
        </div>  
      )
    else if(this.state.type === 'Edge')
      return (
        <div id="informationBox">
          <p>Type: {this.state.type}</p>
          <p>Label: {this.state.name}</p>
          <p>Channel: {`${this.state.channel}`}</p>
        </div> 
      )
  }

  changeTab = (e) => {
    this.setState({tab: e.target.getAttribute('name')})
  }

  tabBar = () => {
    if(this.state.tab === "graph") {
      return <div id="tabBar">
          <h2 className={`tab display`}>Graph</h2>
          <h2 name="stats" className="tab" onClick={this.changeTab}>System Stats</h2>
        </div>
    } else if(this.state.tab === "stats") {
      return <div id="tabBar">
          <h2 name="graph" className={`tab`} onClick={this.changeTab}>Graph</h2>
          <h2 className="tab display">System Stats</h2>
        </div>
    }
  }

  renderGraph = () => {
    return <div id="graphContainer">
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
        <button id="resetButton" onClick={() => this.props.changePage('Landing')}>Reset</button>
      </div>
  </div>
  }

  render () {
    return (
      <div id="graphPage">
        <h1 id="graphTitle">Network Simulation</h1>
        {this.tabBar()}
        {this.state.tab === "graph" ? this.renderGraph() : <StatPage/>}
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
      textRotation: 'autorotate',
      textMarginY: -3,
      textMarginX: 2,
    }
  }
]

