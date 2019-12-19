import React from 'react';
import './styles/index.css'
import '../../node_modules/react-vis/dist/style.css';
import {XYPlot, XAxis, YAxis, ChartLabel, HorizontalGridLines,HorizontalBarSeries,VerticalBarSeries, LineSeries} from 'react-vis';
import Select from 'react-select';

export default class StatPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      chan_switch: [],
      chan_hop: [],
      node_switch: [],
      node_hop: [],
      chan_switch_data: [],
      chan_hop_data: [],
      node_switch_data: [],
      node_hop_data: [],
      data: {},
    }
  }
  async componentDidMount () {
    let stats;
    if(this.props.data) {
      stats = this.props.data;
      this.setState({data:stats});
    } else {
      stats = await fetch('http://127.0.0.1:8081/network_simulator/collect_stats')
      .then(res => res.json())
      .then(data => data)
      .catch(err => err)

      this.setState({data:stats});
    }

    for(const chart in stats) {
      let constants = [];
      let variables = chart.split('_');
      let xVar = variables[0] === "chan" ? "Nodes" : "Channels";
      let yVar = variables[1] === "hop" ? "Switchs" : "Hops";
      for(let constant in stats[chart]) {
        let optionInfo = constant.split('_');
        let option = {
          value:constant,
          label: `${optionInfo[0]} ${xVar} with ${optionInfo[1]} ${yVar}`,
          chart: chart,
        }
        constants.push(option);
      }
      
      this.setState({
        [chart]: constants,
      })
    }
  }

  onSelect = (e) => {
    let dataPoints = this.state.data[e.chart][e.value];
    let data = [];
    for(let point in dataPoints) {
      dataPoints[point].forEach(value => {
         data.push({
          y: value,
          x:parseInt(point),
        })
      })
    }
    let variable = e.chart + '_data';
    this.setState({[variable]: data})
  }

  render() {

    return (
      <div id="statPage">    
        <div className="chart">
          <Select className="select" options={this.state.chan_switch} onChange={this.onSelect} placeholder="Select an option" />
          <XYPlot
            width={400}
            height={200}>
            <HorizontalGridLines />
            <VerticalBarSeries
              barWidth={0.1}
              data={this.state.chan_switch_data}/>
            <XAxis />
            <YAxis />
            <ChartLabel
              text="Number of Channels"
              className="alt-x-label"
              includeMargin={false}
              xPercent={0.35}
              yPercent={1.30}
              />

            <ChartLabel
              text="Channels vs Switches"
              className="chartTitle"
              includeMargin={false}
              xPercent={0.35}
              yPercent={0.05}
              />

            <ChartLabel
              text="Number of Switches"
              className="alt-y-label"
              includeMargin={false}
              xPercent={-0.09}
              yPercent={0.3}
              style={{
                transform: 'rotate(-90)',
                textAnchor: 'end'
              }}
            />
          </XYPlot>
        </div>
        <div className="chart">
        <Select className="select" options={this.state.chan_hop} onChange={this.onSelect} placeholder="Select an option" />
          <XYPlot
            width={400}
            height={200}>
            <HorizontalGridLines />
            <VerticalBarSeries
              barWidth={0.1}
              data={this.state.chan_hop_data}/>
            <XAxis />
            <YAxis />
            <ChartLabel
              text="Number of Channels"
              className="alt-x-label"
              includeMargin={false}
              xPercent={0.35}
              yPercent={1.30}
              />
            
            <ChartLabel
              text="Channels vs Hops"
              className="chartTitle"
              includeMargin={false}
              xPercent={0.35}
              yPercent={0.05}
              />

            <ChartLabel
              text="Number of Hops"
              className="alt-y-label"
              includeMargin={false}
              xPercent={-0.09}
              yPercent={0.3}
              style={{
                transform: 'rotate(-90)',
                textAnchor: 'end'
              }}
            />
          </XYPlot>
        </div>
        <div className="chart">
        <Select name="node_switch" options={this.state.node_switch} onChange={this.onSelect} placeholder="Select an option" />
          <XYPlot
            width={400}
            height={200}>
            <HorizontalGridLines />
            <VerticalBarSeries
              barWidth={0.1}
              data={this.state.node_switch_data}/>
            <XAxis />
            <YAxis />
            <ChartLabel
              text="Number of Nodes"
              className="alt-x-label"
              includeMargin={false}
              xPercent={0.35}
              yPercent={1.30}
              />
            
            <ChartLabel
              text="Nodes vs Switches"
              className="chartTitle"
              includeMargin={false}
              xPercent={0.35}
              yPercent={0.05}
              />

            <ChartLabel
              
              text="Number of Switches"
              className="alt-y-label"
              includeMargin={false}
              xPercent={-0.09}
              yPercent={0.3}
              style={{
                transform: 'rotate(-90)',
                textAnchor: 'end'
              }}
            />
          </XYPlot>
        </div>
        <div className="chart">
        <Select className="select" options={this.state.node_hop} onChange={this.onSelect} placeholder="Select an option" />
          <XYPlot
            width={400}
            height={200}>
            <HorizontalGridLines />
            <VerticalBarSeries
              barWidth={0.1}
              data={this.state.node_hop_data}/>
            <XAxis />
            <YAxis />
            <ChartLabel
              text="Number of Nodes"
              className="alt-x-label"
              includeMargin={false}
              xPercent={0.35}
              yPercent={1.30}
              />
            
            <ChartLabel
              text="Nodes vs Hops"
              className="chartTitle"
              includeMargin={false}
              xPercent={0.35}
              yPercent={0.05}
              />

            <ChartLabel
              text="Number of Hops"
              className="alt-y-label"
              includeMargin={false}
              xPercent={-0.09}
              yPercent={0.3}
              style={{
                transform: 'rotate(-90)',
                textAnchor: 'end'
              }}
            />
          </XYPlot>
        </div>
      </div>
    );
  }
}