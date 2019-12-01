import React from "react";
import LandingPage from './LandingPage';
import GraphPage from './GraphPage'

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
      return <GraphPage data={this.state.data}/>
  }

  render() {
    return(
      <div>
        {this.renderPage()}
      </div>
    )
  }

};
