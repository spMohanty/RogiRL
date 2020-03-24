#!/usr/bin/env python

import numpy as np

from individual import Individual, IndividualStates

class Grid:
    def __init__(
                    self,
                    grid_width = 100,
                    grid_height = 100,
                    number_of_individuals = 100
                ):
        
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.number_of_individuals = number_of_individuals

        self.initialize_individuals_registry()
        self.initialize_grid()
    
    def initialize_grid(self):
        self.grid = []

        for _height in range(self.grid_height):
            self.grid.append([False]*self.grid_width)

    def initialize_individuals_registry(self):
        self.individuals_registry = {
        }
        for _state in IndividualStates:
            self.individuals_registry[_state.name] = {}

    def initialize_individuals(self, number_of_individuals, state=IndividualStates.SUSCEPTIBLE):
        for _ in range(number_of_individuals):
            agent_x, agent_y = self.get_random_empty_cell()
            agent_state = state
            _agent = Individual(
                x = agent_x,
                y = agent_y,
                state = agent_state,
                grid = self
            )
            self.grid[agent_y][agent_x] = _agent
            self.update_agent_state_in_registry(_agent)

    def update_agent_state_in_registry(self, agent):
        # Clean up any previous occurences of agent in registry
        for _state in IndividualStates:
            try:
                foo = self.individuals_registry[_state.name][agent.id]
                del self.individuals_registry[_state.name][agent.id]
            except KeyError:
                continue
        self.individuals_registry[agent.state.name][agent.id] = agent
    
    def get_agents_with_state(self, state=IndividualStates.INFECTIOUS):
        return self.individuals_registry[state.name].values()

    def simulation_step(self):
        #############################################
        #############################################
        # Infect individuals (SUS -> Exposed)
        # Update status of infectious indivuals (to recovered or DEAD)
        # Update status of exposed individuals
        # 
        #############################################
        #############################################
        
        # For all Infectious Indivuals, infect the susceptible indiviuals with a probability p
        infection_probability = 0.2 # beta
        incubation_period_mean = 4 # i_m
        incubation_period_sigma = 1 # i_s
        


        infectious_individuals = get_agents_with_state(IndividualStates.INFECTIOUS)

        for _individual in infectious_individuals:
            # Gather all neighbouring cells
            neighbours = get_individuals_in_neighbouring_cells(
                            _individual.x, 
                            _individual.y, 
                            radius=1)
            
            for _neighbour in neighbours:
                if _neighbour.state == IndividualStates.SUSCEPTIBLE:
                    # Infect them 
                    if np.random.rand() < infection_probability:
                        _neighbour = IndividualStates.EXPOSED
                        self.update_agent_state_in_registry(_neighbour)

    
    ##################################################
    ##################################################
    # Grid Helper Functions
    ##################################################
    ##################################################
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
    
    def get_random_empty_cell(self):
        """
        Returns a random empty cell
        """
        while True:
            agent_x = np.random.randint(self.grid_width)
            agent_y = np.random.randint(self.grid_height)

            if self.grid[agent_y][agent_x]:
                continue
            
            return agent_x, agent_y

    def get_individuals_in_neighbouring_cells(self, x, y, radius=1):
        """
        Returns individuals in the neighbouring cells of radius - r
        
        """
        _individuals = []
        for _x in range(x-radius, x+radius+1):
            for _y in range(y-radius, y+radius+1):
                _x %= self.grid_width
                _y %= self.grid_height

                if self.grid[_y][_x]:
                    _individuals.append(self.grid[_y][_x])
        return _individuals

if __name__ == "__main__":
    grid = Grid(20, 20, 40)
    grid.initialize_individuals(10, IndividualStates.SUSCEPTIBLE)
    grid.initialize_individuals(10, IndividualStates.EXPOSED)
    grid.initialize_individuals(10, IndividualStates.INFECTIOUS)
    grid.initialize_individuals(10, IndividualStates.RECOVERED)
    # grid.initialize_individuals(10, IndividualStates.DEAD)



    grid.render_grid()
    print(grid.individuals_registry)

    # for _agent in grid.individuals:
    #     print(_agent)