'use strict';

class Hexagon extends React.Component {
  render() {
    let translate = `translate(${this.props.x},${this.props.y})`;
    return (
      <g transform={translate}>
        <g stroke="white" strokeWidth="1">
          <polygon points="100,0 50,-87 -50,-87 -100,-0 -50,87 50,87"></polygon>
        </g>
      </g>
    );
  }
};

class Planet extends React.Component {
  render() {
    let translate = `translate(${this.props.x},${this.props.y})`;
    return (
      <g transform={translate}>
        <circle cx="0" cy="0" r="70" stroke="black" strokeWidth="3" fill={this.props.hex_color} />
      </g>
    );
  };
};


class Board extends React.Component {
  componentDidMount() {
    fetch('map').then(results => {
      return results.json();
    }).then(data => {
      console.log(data);
    });
  }

  render() {
    return (
      <svg viewBox="-3000 -1500 6000 3000" xmlns="http://www.w3.org/2000/svg">
        <Hexagon x={0} y={1000} />
        <Planet x={0} y={1000} hex_color={"#ff00ff"} />
      </svg>
    );
  };
};

const domContainer = document.querySelector('#map_container');
ReactDOM.render(React.createElement(Board), domContainer);