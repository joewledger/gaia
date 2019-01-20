'use strict';

const FactionColors = {
  0: 'blue',
  1: 'blue',
  2: 'yellow',
  3: 'yellow',
  4: 'brown',
  5: 'brown',
  6: 'red',
  7: 'red',
  8: 'orange',
  9: 'orange',
  10: 'grey',
  11: 'grey',
  12: 'white',
  13: 'white'
}

const PlanetColors = {
    1: 'red',
    2: "orange",
    3: "white",
    4: "grey",
    5: "yellow",
    6: "brown",
    7: "blue",
    8: "green",
    9: "purple",
    10: "#708090"
}

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
    let buildings = [];

    if (this.props.building !== undefined && this.props.faction !== undefined) {
      buildings.push(<Building type={this.props.building} faction={this.props.faction} />);
    }

    return (
      <g transform={translate}>
        <circle cx="0" cy="0" r="70" stroke="black" strokeWidth="3" fill={PlanetColors[this.props.type]} />
        {buildings}
      </g>
    );
  };
};

class Building extends React.Component {
  render() {
    let faction_color = FactionColors[this.props.faction];
    switch(this.props.type) {
      case(0):
        return(<polyline points="30,-10 30,30 -30,30 -30,-10 0,-30 30,-10" fill={faction_color} stroke="black" strokeWidth="3" />)
        break;
      case(1):
        return(<polyline points="35,-10 35,25 -35,25 -35,-30 -20,-40 0,-30 0,-10 35,-10" fill={faction_color} stroke="black" strokeWidth="3" />)
        break;
      case(2):
        return(<g><circle cx="0" cy="0" r="35" stroke="black" fill={faction_color} strokeWidth="3" /></g>)
        break;
      case(3):
        return(<g><polyline points="36,-36 36,36 -36,36 -36,-36 36,-36" fill={faction_color} stroke="black" strokeWidth="3" /></g>)
        break;
      case(4):
        return(<g><ellipse cx="0" cy="0" rx="50" ry="30" fill={faction_color} stroke="black" strokeWidth="3" /></g>)
        break;
      default:
        return(null)
    }
  }
}

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
              type={planet.planet_type}
              building={planet.building}
              faction={planet.faction} />
    );

    return (
      <g transform={sector_translate}>{hexagons} {planets}</g >
    );
  };
};

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
      board_options: null,
      size: 100,
      sectors: [],
      federations: []
    };

    this.handleChange = this.handleChange.bind(this);
  };

  getMapData() {
    let map_url = `map?game_type=${this.state.game_type}`;
    if(this.state.board_options !=null) {
      map_url += "&board_options=" + this.state.board_options;
    }

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
    let special_game_types = ["lots_o_buildings", "lots_o_federations"];
    let target = event.target.value;

    if(special_game_types.includes(target)) {
      await this.setState({
        game_type: "3p_4p_default",
        board_options: target
      });
    } else {
      await this.setState({
        game_type: target,
        board_options: null
      });
    }

    this.getMapData();
  };

  render() {
    return (
      <div>
        <select onChange={this.handleChange}>
          <option value="1p_2p_default">1p/2p Default</option>
          <option value="3p_4p_default">3p/4p Default</option>
          <option value="lots_o_buildings">lots o' buildings</option>
          <option value="lots_o_federations">lots o' federations</option>
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