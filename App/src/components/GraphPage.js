import React from 'react';
import CytoscapeComponent from "react-cytoscapejs";

export default class GraphPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      source: '',
      target: '',
    }
    this.addLink = this.addLink.bind(this);
    this.sourceInput = this.sourceInput.bind(this);
    this.targetInput = this.targetInput.bind(this);
  }

  addLink = () => {
    let edge= {
      group: "edges",
      data: {
        source: this.state.source,
        target: this.state.target,
        color: 'red',
      }
    }
    this.cy.add(edge);
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

  render () {
    return (
      <div>
        <h1>Network Simulation</h1>
        <input placeholder={"Source"} onChange={this.sourceInput}></input>
        <input placeholder={"Target"} onChange={this.targetInput}></input>
        <button onClick={this.addLink}>Add Link</button>
        <CytoscapeComponent
          cy={(cy) => { this.cy = cy }}
          elements={this.props.data}
          style={{width:500, height:500}}
          pan={ { x: 100, y: 100 } }
          zoom={4}
          stylesheet={[
            {
              selector: 'node[type="device"]',
              style: {
                width: 3,
                height: 3,
                shape: 'rectangle',
                backgroundColor: 'blue',
                label: 'data(label)',
                fontSize: 3,
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
                width: 1,
                curveStyle:'bezier',
                targetArrowShape: 'triangle',
                arrowScale: 0.5,
                lineColor: 'red',
              }
            }
          ]}
        />
      </div>
    );
  }
}

