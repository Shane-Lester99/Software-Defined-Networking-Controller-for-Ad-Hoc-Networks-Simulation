import React from 'react';

class TabBar extends React.Component {
  render() {
    return (
      <div id="tabBar">
          <button id="homeButton" onClick={() => this.props.changePage("Landing")}>Home</button>
      </div>
    );
  }
}

export default TabBar;