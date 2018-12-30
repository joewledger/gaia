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

class Sector extends React.Component {
  render() {
    let size = this.props.size;

    let sector_x_factor = this.props.screen_x_factor * size * .01;
    let sector_y_factor = this.props.screen_y_factor * size * .01;
    let sector_translate = `translate(${sector_x_factor},${sector_y_factor})`;

    let hexagons = [];

    this.props.hexagons.forEach(function(hexagon) {
      let hexagon_x = hexagon.screen_x_factor * size;
      let hexagon_y = hexagon.screen_y_factor * size;

      hexagons.push(<Hexagon x={hexagon_x} y={hexagon_y} />);
    });

    return (
      <g transform={sector_translate}>{hexagons}</g >
    );
  };
};

class Board extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      size: 100,
      sectors: [],
      federations: []
    };
  };

  componentDidMount() {
    fetch('map').then(results => {
      return results.json();
    }).then(data => {
      this.setState({
        sectors: data.sectors,
        federations: data.federations
      });
    });
  };

  render() {
    let sectors = [];
    this.state.sectors.forEach(sector => {
      sectors.push(<Sector hexagons={sector.hexagons}
                           planets={sector.planets}
                           size={100}
                           screen_x_factor={sector.screen_x_factor}
                           screen_y_factor={sector.screen_y_factor} />);
      }
    );

    return (
      <svg viewBox="-3000 -1500 6000 3000" xmlns="http://www.w3.org/2000/svg">
        {sectors}
      </svg>
    );
  };
};

const domContainer = document.querySelector('#map_container');
ReactDOM.render(React.createElement(Board), domContainer);