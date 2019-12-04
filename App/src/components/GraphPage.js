import React from 'react';
import CytoscapeComponent from "react-cytoscapejs";
import Icon from '../../assets/touch-screen.svg';
import data from '../../assets/sampleNodes.json';
import './styles/index.css'

export default class GraphPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      source: '',
      target: '',
      type:'',
      name: '',
      x: '',
      y: '',
      channel: '',
    }
    this.addLink = this.addLink.bind(this);
    this.sourceInput = this.sourceInput.bind(this);
    this.targetInput = this.targetInput.bind(this);
  }

  componentDidMount() {
    this.cy.center();
    this.cy.nodes().ungrabify();
    this.cy.on('click', 'node[type="device"]', function(evt){
      let node = evt.target;
      let id = node.id();
      let position = node.position();
      this.setState({
        type:'Node',
        name: `Node ${id}`,
        x:position.x,
        y:position.y,
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

  addLink = () => {
    let edge= {
      group: "edges",
      data: {
        source: this.state.source,
        target: this.state.target,
        label: `Edge from N${this.state.source} to N${this.state.target}`,
        color: 'red',
      }
    }
    let route;
    try {
      route = require(`../../assets/sampleRoute${this.state.source}${this.state.target}.json`)
    }
    catch {
      alert('Path could not be established');
      return;
    }
    this.cy.add(route);
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
    if(this.state.type === 'Node' || this.state.type === 'Base Station')
      return (
        <div>
          <p>Type: {this.state.type}</p>
          <p>Label: {this.state.name}</p>
          <p>Coordinates: {`[${this.state.x}, ${this.state.y}]`}</p>
        </div>  
      )
    else if(this.state.type === 'Edge')
      return (
        <div>
          <p>Type: {this.state.type}</p>
          <p>Label: {this.state.name}</p>
          <p>Channel: {`${this.state.channel}`}</p>
        </div> 
      )
  }

  render () {
    return (
      <div id="graphPage">
        <h1 id="graphTitle">Network Simulation</h1>
        <div id="graphContainer">
          <CytoscapeComponent
            className={"graph"}
            cy={(cy) => { this.cy = cy }}
            elements={data}
            zoom={5}
            stylesheet={stylesheet}
          />
          <div id="data">
            <div id="addLink">
              <h2>Add Connection</h2>
              <input placeholder={"Source Node"} onChange={this.sourceInput}></input>
              <input placeholder={"Target Node"} onChange={this.targetInput}></input>
              <br/>
              <button id="addButton" onClick={this.addLink}>Add Link</button>
            </div>
            <h2 style={{textAlign:'center'}}>Selected Data</h2>
            {this.getData()}

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
      textRotation: 'autorotate',
      textMarginY: -2,
    }
  }
]

