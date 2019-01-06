from gaia.map import Map

import os
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
valid_moves_example_response = [
    { # Behaves uniquely. Must choose to do before other moves. This must be remembered between player turns. There can be multiple.
        'type': 'leech',
        'player_id': '1234',
        'amount': 3
    },

    {
        'type': 'build',
        'hex': 11,
        'navigation': {'QIC': 2, 'BON11': 1},
        'dig': {'DIG': 3, 'ACT4': 2, 'ACT5': 1}
    },

    {
        'type': 'upgrade',
        'hex': 23,
        'opt1': 1,
        'opt2': None
    },

    {
        'type': 'action',
        'bonus-action': 4
    },

    {
        'type': 'pass',
        'tiles': [1, 5, 7, 11]
    }
]


@api.route('/valid-moves')
class ValidMoves(Resource):
    def get(self):
        return valid_moves_example_response


@api.route('/map')
class Maps(Resource):
    def get(self):
        game_type = request.args.get('game_type', '1p_2p_default')

        map = Map.load_from_config(config_path, game_type=game_type)

        return Response(response=map.to_json(),
                        status=200,
                        mimetype="application/json")
