from enum import Enum
from colors import Colors

COLORS = Colors()
COLOR_MAP = ColorMap()

# Susceptible, Exposed, Infectious, Symptomatic, Recovered/Dead
class RenderConfig(Enum):
    TEXT_LABEL_COLOR = COLOR_MAP.GREY
    