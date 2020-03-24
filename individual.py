#!/usr/bin/env python

import numpy as np
from enum import Enum

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
                grid
                ):
        self.x = x
        self.y = y
        self.grid = grid