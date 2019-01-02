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
        <circle cx="0" cy="0" r="70" stroke="black" strokeWidth="3" fill={this.props.color} />
      </g>
    );
  };
};

class Sector extends React.Component {
  render() {
    let size = this.props.size;
    let sectorStretchFactor = .01;

    let sector_x_factor = this.props.screen_x_factor * size * sectorStretchFactor;
    let sector_y_factor = this.props.screen_y_factor * size * sectorStretchFactor;
    let sector_translate = `translate(${sector_x_factor},${sector_y_factor})`;

    let hexagons = this.props.hexagons.map(hexagon =>
      <Hexagon x={hexagon.screen_x_factor * size}
               y={hexagon.screen_y_factor * size} />
    );

    let planets = this.props.planets.map(planet =>
      <Planet x={planet.hex.screen_x_factor * size}
              y={planet.hex.screen_y_factor * size}
              color={planet.planet_color} />
    );

    return (
      <g transform={sector_translate}>{hexagons} {planets}</g >
    );
  };
};

let getViewboxSize = function(sectors, hexSize) {
  if(sectors.length == 0) {
    return '0 0 0 0';
  }

  let hexagons = sectors.flatMap(sector => sector.hexagons);
  let hex_x = hexagons.map(hex => hex.screen_x_factor);
  let hex_y = hexagons.map(hex => hex.screen_y_factor);

  //accounts for fact that screen_x_factor and screen_y_factor
  //correspond to middle of hex, not edge.
  let viewBoxBorderWidth = 2;

  let min_x = (Math.min(...hex_x) - viewBoxBorderWidth) *  hexSize;
  let max_x = (Math.max(...hex_x) + viewBoxBorderWidth) * hexSize;

  let min_y = (Math.min(...hex_y) - viewBoxBorderWidth) * hexSize;
  let max_y = (Math.max(...hex_y) + viewBoxBorderWidth) * hexSize;

  let width = Math.abs(min_x) + Math.abs(max_x);
  let height = Math.abs(min_y) + Math.abs(max_y);

  return `${min_x} ${min_y} ${width} ${height}`;
}

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
    let sectors = this.state.sectors.map(sector =>
        <Sector hexagons={sector.hexagons}
                planets={sector.planets}
                size={this.state.size}
                screen_x_factor={sector.screen_x_factor}
                screen_y_factor={sector.screen_y_factor} />
    );

    return (
      <svg viewBox={getViewboxSize(this.state.sectors, this.state.size)} xmlns="http://www.w3.org/2000/svg">
        {sectors}
      </svg>
    );
  };
};

const domContainer = document.querySelector('#map_container');
ReactDOM.render(React.createElement(Board), domContainer);