#!/usr/bin/env python

import numpy as np
from enum import Enum
import uuid

class IndividualStates(Enum):
    SUSCEPTIBLE = 1
    EXPOSED = 2
    INFECTIOUS = 3
    RECOVERED = 4
    DEAD = 5


class Individual:
    def __init__(
                self,
                x,
                y,
                state = IndividualStates.SUSCEPTIBLE,
                grid = False
                ):
        self.x = x
        self.y = y
        self.state = state
        self.grid = grid
        self.id = str(uuid.uuid4())

    def __str__(self):
        return "Individual( state={} , x={} , y={} , id={} )".format(self.state.name, self.x, self.y, self.id)

    def __repr__(self):
        return self.__str__()