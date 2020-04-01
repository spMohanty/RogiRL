from enum import Enum

# Susceptible, Exposed, Infectious, Symptomatic, Recovered/Dead
class AgentState(Enum):
    SUSCEPTIBLE = 0 # *
    EXPOSED = 1 # o
    INFECTIOUS = 2 # O
    SYMPTOMATIC = 3 # S
    RECOVERED = 4 # R
    VACCINATED = 5 # V