from gaia.map import Map

import os
import example_responses
from flask import Flask, Response, render_template, request
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)

config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "configs", "board.json")
is_development = os.environ.get("FLASK_DEBUG") == str(1)


# View Routes
@app.route('/board')
def main():
    return render_template("board.html", development=is_development)


# API
@api.route('/valid-moves')
class ValidMoves(Resource):
    def get(self):
        return example_responses.valid_moves_example_response()


@api.route('/map')
class Maps(Resource):
    def get(self):
        game_type = request.args.get('game_type', '1p_2p_default')
        if game_type == 'lots_o_buildings':
            map = Map.load_from_config(config_path, game_type='3p_4p_default')
            map.add_buildings_to_all_planets()
        else:
            map = Map.load_from_config(config_path, game_type=game_type)

        return Response(response=map.to_json(),
                        status=200,
                        mimetype="application/json")
