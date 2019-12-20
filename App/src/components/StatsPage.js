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
      menu2: [],
      menu3: [],
      selection1: '',
      selection2: '',
      selection3: '',
      xAxis: '',
      yAxis:'',
      chartData: [],
      frequencyView: false,
      menu1: [{
        label:"Channels vs Switches",
        value: "chan_switch",
      },
      {
        label:"Channels vs Hops",
        value:"chan_hop"
      },
      {
        label:"Nodes vs Switches",
        value:"node_switch"
      }, {
        label:"Nodes vs Hops",
        value:"node_hop"
      }],
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

  onSelect = (e,num) => {
    if(this.state.frequencyView){
      switch(num) {
        case 1:
          this.setState({
            selection1: e,
            menu2:this.state[e.value],
            selection2: '',
            selection3: '',
            xAxis: '',
            yAxis:'',
            chartData: [],
            menu3: [],
          });
          break;
        case 2:
          let channels = [];
          for(let channel in this.state.data[this.state.selection1.value][e.value]) {
            if(this.state.selection1.value[0] === 'c')
            channels.push({
              value:channel,
              label: channel + " Channels",
            })
            else
            channels.push({
              value:channel,
              label: channel + " Nodes",
            })
          }
          this.setState({
            selection2: e,
            menu3:channels,
            selection3: '',
            xAxis: '',
            yAxis:'',
            chartData: [],
          })
          break;
        case 3:
          let xAxis;
          let yAxis = "Frequency";
          if(this.state.selection1.value[this.state.selection1.value.length-1] === 'p')
            xAxis = "Number of Hops";
          else
            xAxis = "Number of Switches";
          let chartData = {};
          this.state.data[this.state.selection1.value][this.state.selection2.value][e.value].forEach(value => {
            if(chartData[value] === undefined) {
              chartData[value] = {
                x: value,
                y: 1,
              }
            } else {
              chartData[value].y += 1;
            }
          })
          let data = []
          for(let point in chartData) {
            data.push(chartData[point]);
          }
          this.setState({xAxis,yAxis,chartData: data,selection3: e});
          break;
      }
    } else {
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
    
  }

  frequencyView = () => {
    if(this.state.frequencyView) {
      return (<div id="frequencyView">
        <Select className="select" options={this.state.menu1} value={this.state.selection1} onChange={(e) => this.onSelect(e,1)} placeholder="Select an option" />
        <Select className="select" options={this.state.menu2} value={this.state.selection2} onChange={(e) => this.onSelect(e,2)} placeholder="Select an option" />
        <Select className="select" options={this.state.menu3} value={this.state.selection3} onChange={(e) => this.onSelect(e,3)} placeholder="Select an option" />
        <XYPlot
          width={400}
          height={200}>
          <HorizontalGridLines />
          <VerticalBarSeries
            barWidth={0.1}
            data={this.state.chartData}/>
          <XAxis />
          <YAxis />
          <ChartLabel
            text={this.state.xAxis}
            className="alt-x-label"
            includeMargin={false}
            xPercent={0.35}
            yPercent={1.30}
            />

          <ChartLabel
            text={this.state.selection1.label}
            className="chartTitle"
            includeMargin={false}
            xPercent={0.35}
            yPercent={0.05}
            />

          <ChartLabel
            text={this.state.yAxis}
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
      </div>)
    }
  }

  standardView = () => {
    if(!this.state.frequencyView) {
      return(
        <div id="chartContainer">
          <div className="chart">
          <Select className="select" options={this.state.chan_switch} onChange={this.onSelect} placeholder="Select an option" />
          <XYPlot
            width={400}
            height={175}>
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
          <br/>
          <XYPlot
            width={400}
            height={175}>
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
         <Select className="select" options={this.state.node_switch} onChange={this.onSelect} placeholder="Select an option" />
          <XYPlot
            width={400}
            height={175}>
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
            height={175}>
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
      )
    }
  }

  render() {

    return (
      <div id="statPage">
        <button id="toggleView" onClick={()=>{this.setState({frequencyView:!this.state.frequencyView})}}>Toggle View</button>
        {this.state.frequencyView ? this.frequencyView() : this.standardView()}
      </div>
    );
  }
}