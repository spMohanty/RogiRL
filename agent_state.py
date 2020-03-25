from enum import Enum

# Susceptible, Exposed, Infectious, Symptomatic, Recovered/Dead
class AgentState(Enum):
    SUSCEPTIBLE = 0
    EXPOSED = 1
    INFECTIOUS = 2
    SYMPTOMATIC = 3
    RECOVERED = 4
    DEAD = 5
