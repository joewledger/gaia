from gaia.map import Map

import os
from flask import Flask, Response
app = Flask(__name__)

config_path = os.path.dirname(os.path.realpath(__file__)) + "\\configs\\board.json"


@app.route('/map')
def get_map():
    map_json = Map.load_from_config(config_path, game_type="2p_default").to_json()

    return Response(response=map_json,
                    status=200,
                    mimetype="application/json")
