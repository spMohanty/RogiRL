"""
Configure visualization elements and instantiate a server
"""

try:
    from disease_sim.model import DiseaseSimModel, DiseaseSimAgent  # noqa
    from disease_sim.colors import ColorMap
except ImportError:
    from model import DiseaseSimModel, DiseaseSimAgent  # noqa
    from colors import ColorMap

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

COLOR_MAP = ColorMap()

def agent_potrayal(agent):
    if agent is None:
        return

    portrayal = {
                    "Shape": "rect",
                    "Filled": "true",
                    "w" : 0.8,
                    "h" : 0.8,
                    "id" : agent.unique_id,
                    "state" : agent.state.name,
                    "Layer" : 0,
                    "Color": "rgb{}".format(COLOR_MAP.get_color(agent.state))
                 }
    return portrayal


grid_width = 50
grid_height = 50

canvas_width = 500
canvas_height = 500

canvas_element = CanvasGrid(agent_potrayal, grid_width, grid_height, canvas_width, canvas_height)
chart_element = ChartModule([{"Label": "DiseaseSim", "Color": "Pink"}])

model_kwargs = {
                    "n_agents": 1000,
                    "width": grid_width,
                    "height": grid_height,
                    "prob_agent_movement" : 0.1
                }

server = ModularServer(DiseaseSimModel, [canvas_element, chart_element],  # noqa
                       "DiseaseSim", model_kwargs)
