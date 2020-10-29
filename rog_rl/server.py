"""
Configure visualization elements and instantiate a server
"""

from rog_rl.model import DiseaseSimModel, DiseaseSimAgent  # noqa
from rog_rl.colors import ColorMap
from rog_rl.agent_state import AgentState

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

COLOR_MAP = ColorMap()


def agent_potrayal(agent):
    if agent is None:
        return

    portrayal = {
                    "Shape": "circle",
                    "Filled": "true",
                    "r": 0.9,
                    "id": agent.unique_id,
                    "state": agent.state.name,
                    "Layer": 0,
                    "Color": "rgb{}".format(COLOR_MAP.get_color(agent.state))
                 }
    return portrayal


def build_server(grid_width=50, grid_height=50):
    canvas_width = 500
    canvas_height = 500

    canvas_element = CanvasGrid(
                        agent_potrayal, grid_width, grid_height,
                        canvas_width, canvas_height)
    chart_element = ChartModule([
                                    {
                                        "Label": "Susceptible",
                                        "Color": "rgb{}".format(
                                            COLOR_MAP.get_color(
                                                AgentState.SUSCEPTIBLE))
                                    },
                                    {
                                        "Label": "Exposed",
                                        "Color": "rgb{}".format(
                                            COLOR_MAP.get_color(
                                                AgentState.EXPOSED))
                                    },
                                    {
                                        "Label": "Infectious",
                                        "Color": "rgb{}".format(
                                            COLOR_MAP.get_color(
                                                AgentState.INFECTIOUS))
                                    },
                                    {
                                        "Label": "Symptomatic",
                                        "Color": "rgb{}".format(
                                            COLOR_MAP.get_color(
                                                AgentState.SYMPTOMATIC))
                                    },
                                    {
                                        "Label": "Recovered",
                                        "Color": "rgb{}".format(
                                            COLOR_MAP.get_color(
                                                AgentState.RECOVERED))
                                    },
                                    {
                                        "Label": "Vaccinated",
                                        "Color": "rgb{}".format(
                                            COLOR_MAP.get_color(
                                                AgentState.VACCINATED))
                                    },
                                    {
                                        "Label": "R0/10",
                                        "Color": "rgb{}".format(
                                            COLOR_MAP.get_color(
                                                "R0/10"
                                            )
                                        )
                                    }
                                ])
    model_params = {
        "width": grid_width,
        "height": grid_height,
        "population_density": UserSettableParameter(
                    'slider', 'Population Density', value=1.0,
                    min_value=0.01, max_value=1.0, step=0.01
                    ),
        "vaccine_density": UserSettableParameter(
                    'slider', 'Vaccine Density', value=0.0,
                    min_value=0.0, max_value=0.99, step=0.01
                    ),
        "initial_infection_fraction":
            UserSettableParameter(
                    'slider', 'Initial Infection Fraction', value=0.05,
                    min_value=0.01, max_value=0.99, step=0.01
                    ),
        "initial_vaccination_fraction":
            UserSettableParameter(
                    'slider', 'Initial Vaccination Fraction', value=0.00,
                    min_value=0.00, max_value=0.99, step=0.01
                    ),
        "prob_infection":
            UserSettableParameter(
                    'slider', 'Infection Probability', value=0.05,
                    min_value=0.01, max_value=1.0, step=0.01
                    ),
        "prob_agent_movement":
            UserSettableParameter(
                    'slider', 'Movement Probability', value=0.1,
                    min_value=0.00, max_value=1.0, step=0.01
                    ),
        "max_timesteps": UserSettableParameter(
                                                'number', 'Max. Timesteps',
                                                value=200),
        "early_stopping_patience": UserSettableParameter(
                                                'number',
                                                'Early Stopping Patience',
                                                value=14),
        "toric": UserSettableParameter('checkbox', 'Toric Grid', value=True),
        "seed": UserSettableParameter('number', 'Seed', value=420),
    }

    _server = ModularServer(DiseaseSimModel, [canvas_element, chart_element],  # noqa
                            "Rog Simulator", model_params)

    return _server


server = build_server()
