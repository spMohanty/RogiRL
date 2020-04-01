"""
Configure visualization elements and instantiate a server
"""

try:
    from .model import DiseaseSimModel, DiseaseSimAgent  # noqa
except ImportError:
    from model import DiseaseSimModel, DiseaseSimAgent  # noqa

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule


def agent_potrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5,
                 "Color": "#ff0000"}
    return portrayal


grid_width = 50
grid_height = 50

canvas_width = 500
canvas_height = 500

canvas_element = CanvasGrid(agent_potrayal, grid_width, grid_height, canvas_width, canvas_height)
chart_element = ChartModule([{"Label": "DiseaseSim", "Color": "Pink"}])

model_kwargs = {"n_agents": 1000,
                "width": grid_width,
                "height": grid_height}

server = ModularServer(DiseaseSimModel, [canvas_element, chart_element],  # noqa
                       "DiseaseSim", model_kwargs)
