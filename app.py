from gaia.map import Map

import os
from flask import Flask, Response, render_template, request
app = Flask(__name__)

config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "configs", "board.json")
is_development = os.environ.get("FLASK_DEBUG") == 1


@app.route('/')
def main():
    return render_template("board.html", development=is_development)


@app.route('/map')
def get_map():
    game_type = request.args.get('game_type', '1p_2p_default')

    map = Map.load_from_config(config_path, game_type=game_type)

    return Response(response=map.to_json(),
                    status=200,
                    mimetype="application/json")
