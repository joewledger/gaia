'use strict';

class Hexagon extends React.Component {
  render() {
    let translate = `translate(${this.props.x},${this.props.y})`;
    return (
      <g transform={translate}>
          <polygon points="100,0 50,-87 -50,-87 -100,-0 -50,87 50,87"></polygon>
      </g>
    );
  }
};

class Board extends React.Component {
  render() {
    return (
      <svg viewBox="-3000 -1500 6000 3000" xmlns="http://www.w3.org/2000/svg">
        <Hexagon x={0} y={1000} />
      </svg>
    );
  };
};

const domContainer = document.querySelector('#map_container');
ReactDOM.render(React.createElement(Board), domContainer);