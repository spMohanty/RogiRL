#!/usr/bin/env python
import numpy as np

from agent_state import AgentState
from agent import Agent
from coordinate import Coordinate
from grid import Grid

from disease_scheduler import SimpleSEIRDiseaseScheduler

class DiseaseEngine:
    def __init__(   self, 
                    grid_width=100, 
                    grid_height=100, 
                    n_agents=10,
                    initial_infection_fraction=0.2,
                    prob_infection=0.2,
                    toric_grid=True,
                    seed = False
                ):

        self.grid_width = grid_width
        self.grid_height = grid_height
        self.n_agents = n_agents
        self.initial_infection_fraction = initial_infection_fraction
        self.prob_infection = prob_infection
        self.toric_grid = toric_grid

        self.timestep = 0

        self.np_random = np.random
        if seed != False:
            self.np_random.seed(seed)

        self.initialize_grid()
        self.initialize_agent_registry()
        self.initialize_agents()
        self.initialize_disease_scheduler()

        self.initialize_infection()

    def initialize_grid(self):
        self.grid = Grid(
            self.grid_width,
            self.grid_height,
            self.n_agents,
            self.toric_grid,
            self.np_random
        )
    
    def initialize_agents(self):
        # Initialize the whole grid with agents
        # for x in range(self.grid_width):
        #     for y in range(self.grid_height):
        #         _agent = Agent(Coordinate(x,y))
        #         self.grid.set_agent(_agent)
        # print(self.grid)
        empty_cells = self.grid.get_random_empty_cells(n_cells=self.n_agents)
        for n in range(self.n_agents):
            _agent = Agent(empty_cells[n])
            self.grid.set_agent(_agent)
            self.update_agent_in_registry(_agent)

    def initialize_agent_registry(self):
        self.agent_registry = {}
        for state_name in AgentState:
            self.agent_registry[state_name] = {}

    def initialize_disease_scheduler(self):
        self.disease_scheduler = \
            SimpleSEIRDiseaseScheduler(np_random=self.np_random)

    def update_agent_in_registry(self, agent):
        # If there are any previous instances of agents, then delete them
        for state_name in AgentState:
            try:
                del self.agent_registry[state_name][agent.uid]
            except KeyError:
                pass
        self.agent_registry[agent.state][agent.uid] = agent

    def get_agents_with_state(self, state):
        return list(self.agent_registry[state].values())

    def trigger_infection(self, agent, prob_infection):
        if self.np_random.rand() < prob_infection:
            disease_schedule = self.disease_scheduler.get_disease_schedule(
                                    base_timestep=self.timestep)
            agent.register_events(disease_schedule)
            self.update_agent_in_registry(agent)

    def initialize_infection(self):
        """
            Initializes infection in a fraction of the susceptible population
        """
        initial_infection_fraction = self.initial_infection_fraction
        susceptible_agents = self.get_agents_with_state(AgentState.SUSCEPTIBLE)

        number_of_agents_to_infect = int(self.initial_infection_fraction * len(susceptible_agents))
        self.np_random.shuffle(susceptible_agents)
        for k in range(number_of_agents_to_infect):
            _agent = susceptible_agents[k]
            self.trigger_infection(_agent, prob_infection=1.0)
            _agent.process_events()

if __name__ == "__main__":

    disease_engine = DiseaseEngine(
                            grid_width=10,
                            grid_height=10,
                            n_agents=100,
                            initial_infection_fraction=0.05,
                            prob_infection=1.0
                            )
    print(disease_engine.grid)
