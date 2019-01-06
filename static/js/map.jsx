'use strict';

class Hexagon extends React.Component {
  render() {
    let translate = `translate(${this.props.x},${this.props.y})`;
    let poly_id = `(${this.props.hex_x},${this.props.hex_z})`;
    return (
      <g transform={translate}>
        <g stroke="white" strokeWidth="1">
          <polygon id={poly_id} points="100,0 50,-87 -50,-87 -100,-0 -50,87 50,87"></polygon>
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
               y={hexagon.screen_y_factor * size}
               hex_x={hexagon.x}
               hex_z={hexagon.z} />
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
  render() {
    let sectors = this.props.sectors.map(sector =>
        <Sector hexagons={sector.hexagons}
                planets={sector.planets}
                size={this.props.size}
                screen_x_factor={sector.screen_x_factor}
                screen_y_factor={sector.screen_y_factor} />
    );

    return (
      <svg viewBox={getViewboxSize(this.props.sectors, this.props.size)} xmlns="http://www.w3.org/2000/svg">
        {sectors}
      </svg>
    );
  };
};

class BoardSelector extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      game_type: '1p_2p_default',
      size: 100,
      sectors: [],
      federations: []
    };

    this.handleChange = this.handleChange.bind(this);
  };

  getMapData() {
    let map_url = `map?game_type=${this.state.game_type}`;

    fetch(map_url).then(results => {
      return results.json();
    }).then(data => {
      this.setState({
        sectors: data.sectors,
        federations: data.federations
      });
    });
  }

  componentDidMount() {
    this.getMapData();
  };

  async handleChange(event) {
    await this.setState({
      game_type: event.target.value
    });

    this.getMapData();
  };

  render() {
    return (
      <div>
        <select onChange={this.handleChange}>
          <option value="1p_2p_default">1p/2p Default</option>
          <option value="3p_4p_default">3p/4p Default</option>
          <option value="lots_o_buildings">lots o' buildings</option>
        </select>
        <Board size={this.state.size}
               sectors={this.state.sectors}
               federations={this.state.federations} />
      </div>
    );
  };
};

const domContainer = document.querySelector('#map_container');
ReactDOM.render(React.createElement(BoardSelector), domContainer);