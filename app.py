from gaia.map import HexagonGrid

from flask import Flask
app = Flask(__name__)


@app.route('/')
def draw_map():
    return str(HexagonGrid(1))
