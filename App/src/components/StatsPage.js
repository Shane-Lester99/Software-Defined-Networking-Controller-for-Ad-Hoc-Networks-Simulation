import React from 'react';
import chartData from '../../assets/charts.json';
import './styles/index.css'
import '../../node_modules/react-vis/dist/style.css';
import {XYPlot, XAxis, YAxis, ChartLabel, HorizontalGridLines,HorizontalBarSeries,VerticalBarSeries, LineSeries} from 'react-vis';

export default class StatPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      chan_switch: [],
      chan_hop: [],
      node_switch: [],
      node_hop: [],
    }
  }
  componentDidMount() {

  }

  render() {
    return (
      <div id="statPage">
        <div className="chart">
          <XYPlot
            width={400}
            height={200}>
            <HorizontalGridLines />
            <HorizontalBarSeries
              data={[
                {x: 10, y: 1},
                {x: 5, y: 2},
                {x: 15, y: 3}
              ]}/>
            <XAxis />
            <YAxis tickValues={[0, 1, 2, 3, 4]}/>
            <ChartLabel
              text="Number of Switches"
              className="alt-x-label"
              includeMargin={false}
              xPercent={0.4}
              yPercent={1.30}
              />

            <ChartLabel
              text="Number of Channels"
              className="alt-y-label"
              includeMargin={false}
              xPercent={-0.09}
              yPercent={0.4}
              style={{
                transform: 'rotate(-90)',
                textAnchor: 'end'
              }}
            />
          </XYPlot>
        </div>
        <div className="chart">
          <XYPlot
            width={400}
            height={200}>
            <HorizontalGridLines />
            <HorizontalBarSeries
              data={[
                {x: 10, y: 1},
                {x: 5, y: 2},
                {x: 15, y: 3}
              ]}/>
            <XAxis />
            <YAxis tickValues={[0, 1, 2, 3, 4]}/>
            <ChartLabel
              text="Number of Hops"
              className="alt-x-label"
              includeMargin={false}
              xPercent={0.4}
              yPercent={1.30}
              />

            <ChartLabel
              text="Number of Channels"
              className="alt-y-label"
              includeMargin={false}
              xPercent={-0.09}
              yPercent={0.4}
              style={{
                transform: 'rotate(-90)',
                textAnchor: 'end'
              }}
            />
          </XYPlot>
        </div>
        <div className="chart">
          <XYPlot
            width={400}
            height={200}>
            <HorizontalGridLines />
            <HorizontalBarSeries
              data={[
                {x: 10, y: 1},
                {x: 5, y: 2},
                {x: 15, y: 3}
              ]}/>
            <XAxis />
            <YAxis tickValues={[0, 1, 2, 3, 4]}/>
            <ChartLabel
              text="Number of Switches"
              className="alt-x-label"
              includeMargin={false}
              xPercent={0.4}
              yPercent={1.30}
              />

            <ChartLabel
              text="Number of Nodes"
              className="alt-y-label"
              includeMargin={false}
              xPercent={-0.09}
              yPercent={0.4}
              style={{
                transform: 'rotate(-90)',
                textAnchor: 'end'
              }}
            />
          </XYPlot>
        </div>
        <div className="chart">
          <XYPlot
            width={400}
            height={200}>
            <HorizontalGridLines />
            <HorizontalBarSeries
              data={[
                {x: 10, y: 1},
                {x: 5, y: 2},
                {x: 15, y: 3}
              ]}/>
            <XAxis />
            <YAxis tickValues={[0, 1, 2, 3, 4]}/>
            <ChartLabel
              text="Number of Hops"
              className="alt-x-label"
              includeMargin={false}
              xPercent={0.4}
              yPercent={1.30}
              />

            <ChartLabel
              text="Number of Nodes"
              className="alt-y-label"
              includeMargin={false}
              xPercent={-0.09}
              yPercent={0.4}
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