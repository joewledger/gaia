from gaia.map import Hexagon

from flask import Flask
app = Flask(__name__)


@app.route('/')
def draw_map():
    return str(Hexagon(1, 2))
