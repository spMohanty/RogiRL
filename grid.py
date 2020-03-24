#!/usr/bin/env python

import numpy as np

from individual import Individual, IndividualStates

class Grid:
    def __init__(
                    self,
                    grid_width = 100,
                    grid_height = 100,
                    number_of_agents = 100
                ):
        
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.number_of_agents = number_of_agents
        self.agents = []

        self.initialize_grid()
    
    def initialize_grid(self):
        self.grid = []

        for _height in range(self.grid_height):
            self.grid.append([False]*self.grid_width)

    def initialize_agents(self, number_of_agents, state=IndividualStates.SUSCEPTIBLE):
        for _ in range(number_of_agents):
            agent_x, agent_y = self.get_random_empty_cell()
            agent_state = state
            _agent = Individual(
                x = agent_x,
                y = agent_y,
                state = agent_state,
                grid = self
            )
            self.grid[agent_y][agent_x] = _agent
            self.agents.append(_agent)

    def render_grid(self, mode="ascii"):

        # ASCII mode
        print()
        for _y in range(self.grid_height):
            print("| ", end="")
            for _x in range(self.grid_width):
                # Case of empty grid
                if self.grid[_y][_x] == False:
                    print("-", end=" ")
                elif type(self.grid[_y][_x]) == Individual:
                    individual = self.grid[_y][_x]
                    if individual.state == IndividualStates.SUSCEPTIBLE:
                        print("S", end=" ")
                    elif individual.state == IndividualStates.EXPOSED:
                        print("E", end=" ")
                    elif individual.state == IndividualStates.INFECTIOUS:
                        print("I", end=" ")
                    elif individual.state == IndividualStates.RECOVERED:
                        print("R", end=" ")
                    elif individual.state == IndividualStates.DEAD:
                        print("X", end=" ")
                    else:
                        raise NotImplementedError("Unknown State Received")

            print("|")
        print("  " + "_ "*self.grid_width)
    
    ##################################################
    ##################################################
    # Grid Helper Functions
    ##################################################
    ##################################################
    def get_random_empty_cell(self):
        
        while True:
            agent_x = np.random.randint(self.grid_width)
            agent_y = np.random.randint(self.grid_height)

            if self.grid[agent_y][agent_x]:
                continue
            
            return agent_x, agent_y
    
if __name__ == "__main__":
    grid = Grid(20, 20, 40)
    grid.initialize_agents(10, IndividualStates.SUSCEPTIBLE)
    grid.initialize_agents(10, IndividualStates.EXPOSED)
    grid.initialize_agents(10, IndividualStates.INFECTIOUS)
    grid.initialize_agents(10, IndividualStates.RECOVERED)
    grid.initialize_agents(10, IndividualStates.DEAD)
    grid.render_grid()