import React from "react";
import LandingPage from './LandingPage';
import GraphPage from './GraphPage'
import TabBar from './TabBar'
import './styles/index.css'


export default class App extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      page: "Landing",
      data: [],
    }
    this.changePage = this.changePage.bind(this);
    this.renderPage = this.renderPage.bind(this);
  }

  changePage = (page) => {
    this.setState({
      page: page,
    })
  }
  
  setData = (data) => {
    this.setState({
      data: data,
    })
  }

  renderPage = () => {
    if(this.state.page === "Landing")
      return <LandingPage changePage={this.changePage} setData={this.setData}/>
    else(this.state.page === "Graph")
      return <GraphPage changePage={this.changePage} data={this.state.data}/>
  }

  render() {
    return(
      <div id="page">
        <TabBar changePage={this.changePage}/>
        {this.renderPage()}
      </div>
    )
  }

};
