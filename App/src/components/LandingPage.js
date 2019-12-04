import React from 'react';
import './styles/index.css';

class LandingPage extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
      numberOfNodes: 5,
      numberOfBaseStations: 0,
      elements: [],
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
    let elements = [];
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
    /*
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
    this.props.setData(elements);
    this.props.changePage("Graph");
  }

  nodeInput (e) {
    if(!isNaN(e.target.value) && parseInt(e.target.value) <= 10 && parseInt(e.target.value) > 0)
      this.setState({
        numberOfNodes: parseInt(e.target.value),
      })
  }

  baseStationInput (e) {
    if(!isNaN(e.target.value) && parseInt(e.target.value) <= 3 && parseInt(e.target.value) > 0)
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
          <input placeholder={'Number of Nodes'} onChange={this.nodeInput} />
          <br/>
          <input placeholder={'Number of Base Stations'} onChange={this.baseStationInput}/>
          <br/>
          <button id="randomizeButton" onClick={this.randomize}>Randomize</button>
        </div>
      </div>
    )
  }
}

export default LandingPage;