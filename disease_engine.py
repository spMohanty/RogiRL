#!/usr/bin/env python
import numpy as np

from agent_state import AgentState
from agent import Agent
from coordinate import Coordinate
from grid import Grid

import time

from disease_scheduler import SimpleSEIRDiseaseScheduler

class DiseaseEngine:
    def __init__(   self, 
                    grid_width=100, 
                    grid_height=100, 
                    n_agents=10,
                    initial_infection_fraction=0.2,
                    prob_infection=0.2,
                    prob_agent_movement=0.1,
                    toric_grid=True,
                    seed = False
                ):

        self.grid_width = grid_width
        self.grid_height = grid_height
        self.n_agents = n_agents
        self.initial_infection_fraction = initial_infection_fraction
        self.prob_infection = prob_infection
        self.prob_agent_movement = prob_agent_movement
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
            # _agent.process_events()
    def print_stats(self):
        stats = ""
        stats += "="*10 + "\n"
        stats += "="*10 + "\n"
        for state_name in AgentState:
            stats += "{}:\t{}\n".format(state_name,len(self.agent_registry[state_name]))
        stats += "="*10 + "\n"
        print(stats)
    
    def vaccinate_cell(self, coord: Coordinate):
        """
        Vaccinates the agent at a cell if applicable
        """
        # if cell is empty, return -1
        # if cell is anything but susceptible, return -1
        # if cell is susceptible : return 1

        potential_agent = self.grid.get_agent(coord)
        if not potential_agent:
            # Empty Cell
            return False, -10
        else:
            # Agent Found
            if potential_agent.state == AgentState.SUSCEPTIBLE:
                potential_agent.set_state(AgentState.VACCINATED)
                self.grid.set_agent(potential_agent)
                return True, 10
            else: 
                # Agent does not need vaccination
                return False, -5


    def tick(self):
        ########################################
        # Spread Infection
        #
        # - For all infectious agents, 
        #   infect the neighbouring cells with relevant prob
        ########################################
        ########################################
        valid_infectious_agents = []
        valid_infectious_agents += self.get_agents_with_state(AgentState.INFECTIOUS)
        valid_infectious_agents += self.get_agents_with_state(AgentState.SYMPTOMATIC)

        for _infectious_agent in valid_infectious_agents:
            target_candidates = self.grid.get_all_neighbours(_infectious_agent.coordinate)
            # print(target_candidates)
            for _target_candidate in target_candidates:
                if _target_candidate and _target_candidate.state == AgentState.SUSCEPTIBLE:
                    #print("Trying to infect : ", _target_candidate)
                    self.trigger_infection(_target_candidate, prob_infection=self.prob_infection)

        ########################################
        ########################################
        # Tick all agents
        #
        ########################################
        ########################################
        all_agents = []
        for state_name in AgentState:
            all_agents += self.agent_registry[state_name].values()

        for _agent in all_agents:
            _agent.tick()
            self.update_agent_in_registry(_agent)

        ########################################
        ########################################
        # Random Walk of all agents 
        # - if applicable
        ########################################
        ########################################
        for _agent in all_agents:
            if self.np_random.rand() < self.prob_agent_movement:
                empty_cell = self.grid.get_random_empty_neighbouring_cell(_agent.coordinate)
                if empty_cell:
                    self.grid.clear_cell(_agent.coordinate)
                    _agent.move_to(empty_cell)
                    self.grid.set_agent(_agent)
        
        self.timestep += 1 

if __name__ == "__main__":

    disease_engine = DiseaseEngine(
                            grid_width=30,
                            grid_height=30,
                            n_agents=200,
                            initial_infection_fraction=0.04,
                            prob_infection=0.2,
                            prob_agent_movement=0.5
                            )
    # print(disease_engine.grid)
    # print(disease_engine.grid.get_all_neighbours(Coordinate(0,0)))

    # Vaccinate some individuals
    for _agent in disease_engine.agent_registry[AgentState.SUSCEPTIBLE].values():
        if disease_engine.np_random.rand() < 0.1:
            disease_engine.vaccinate_cell(_agent.coordinate)

    print(disease_engine.grid)
    _time = time.time()
    for k in range(100):
        print("Timestep : {}".format(disease_engine.timestep))
        disease_engine.tick()
        print(disease_engine.grid)
        print(time.time() - _time)
        print(disease_engine.print_stats())
        _time = time.time()
        time.sleep(0.1)
        # print(disease_engine.agent_registry)
