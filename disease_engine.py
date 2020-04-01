#!/usr/bin/env python
import numpy as np

from agent_state import AgentState
from agent import Agent
from coordinate import Coordinate
from grid import Grid

from colors import ColorMap
COLOR_MAP = ColorMap()

from renderer import Renderer

import time

from disease_scheduler import SimpleSEIRDiseaseScheduler, SEIRDiseaseScheduler

class DiseaseEngine:
    def __init__(   self, 
                    grid_width=50, 
                    grid_height=50, 
                    n_agents=1500,
                    n_vaccines=100,
                    initial_infection_fraction=0.2,
                    initial_vaccination_fraction=0.05,
                    prob_infection=0.2,
                    prob_agent_movement=0.1,
                    disease_scheduler="simple_seir",
                    max_timesteps=200,
                    toric_grid=True,
                    use_renderer=False,
                    seed = False
                ):

        self.grid_width = grid_width
        self.grid_height = grid_height
        self.n_agents = n_agents
        self.n_vaccines = n_vaccines
        self.initial_infection_fraction = initial_infection_fraction
        self.initial_vaccination_fraction = initial_vaccination_fraction

        self.prob_infection = prob_infection
        self.prob_agent_movement = prob_agent_movement
        self.toric_grid = toric_grid
        self.use_renderer = use_renderer

        self.max_timesteps = max_timesteps
        self.timestep = 0
        self.env_steps = 0

        self.np_random = np.random
        if seed != False:
            self.np_random.seed(seed)

        self.initialize_grid()
        self.initialize_renderer()
        self.initialize_agent_registry()
        self.initialize_disease_scheduler(disease_scheduler)
        self.initialize_agents()

        self.initialize_infection()
        self.initialize_vaccination()

        self.tick()

    def initialize_grid(self):
        self.grid = Grid(
            self.grid_width,
            self.grid_height,
            self.n_agents,
            self.toric_grid,
            self.np_random
        )
    def initialize_renderer(self):
        if self.use_renderer:
            self.renderer = Renderer(
                    grid_size=(self.grid_width, self.grid_height)
                )
            self.renderer.setup()
        else:
            self.renderer = False
    
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

    def initialize_vaccination(self):
        # Vaccinate some individuals
        for _agent in self.agent_registry[AgentState.SUSCEPTIBLE].values():
            if self.np_random.rand() < self.initial_vaccination_fraction:
                self.vaccinate_cell(_agent.coordinate)

        # Update no of vaccines on renderer
        if self.renderer:
            print("Vaccines Left : ", self.n_vaccines)
            self.renderer.update_stats("VACCINE_BUDGET","{}".format(self.n_vaccines, 0))

    def initialize_agent_registry(self):
        self.agent_registry = {}
        for state_name in AgentState:
            self.agent_registry[state_name] = {}

    def initialize_disease_scheduler(self, scheduler_name="simple_seir"):
        if scheduler_name == "simple_seir":
            self.disease_scheduler = \
                SimpleSEIRDiseaseScheduler(np_random=self.np_random)
        elif scheduler_name == "seir":
            self.disease_scheduler = \
                SEIRDiseaseScheduler(np_random=self.np_random)
        else:
            raise NotImplementedError()

    def update_renderer(self):
        """
        Updates the latest board state on the renderer
        """
        ACTIONS = []
        if self.use_renderer:
            # Draw Renderer
            # Update Renderer State 
            total_cases = sum([len(x) for x in self.agent_registry.values()])
            for _state in self.agent_registry.keys():
                self.renderer.update_stats(
                    _state,
                    "{} ({:.2f}%)".format(
                        len(self.agent_registry[_state]),
                        (len(self.agent_registry[_state]) / total_cases) * 100
                    )
                )

            # Update the rest of the renderer
            ACTIONS += self.renderer.pre_render()
            for _state in self.agent_registry.keys():
                for _agent_uid in self.agent_registry[_state]:
                    _agent = self.agent_registry[_state][_agent_uid]
                    _state = _agent.state
                    color = COLOR_MAP.get_color(_state)
                    self.renderer.draw_cell(
                        _agent.coordinate.x, _agent.coordinate.y,
                        color
                    )
            self.renderer.post_render()
        
        return ACTIONS
        



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
        if not agent.is_disease_scheduled() and self.np_random.rand() < prob_infection:
            disease_schedule = self.disease_scheduler.get_disease_schedule(
                                    base_timestep=self.timestep)
            agent.register_disease_events(disease_schedule)
            self.update_agent_in_registry(agent)
            # if self.timestep == 0:
            #     agent.process_events()

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
            
    def update_stats(self):
        self._stats = {}
        for state_name in AgentState:
            self._stats[state_name] = len(self.agent_registry[state_name])
        
    def get_stats(self):
        self.update_stats()
        return self._stats
        
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

        self.env_steps += 1
        if self.renderer:
            self.renderer.update_stats("GAME_TICKS","{}".format(self.env_steps))


        if self.n_vaccines > 0:
            self.n_vaccines -= 1
            # Update no of vaccines on renderer
            if self.renderer:
                print("Vaccines Left : ", self.n_vaccines)
                self.renderer.update_stats("VACCINE_BUDGET","{}".format(self.n_vaccines, 0))

            if not potential_agent:
                # Empty Cell
                return False, -10
            else:
                # Agent Found
                if potential_agent.state == AgentState.SUSCEPTIBLE:
                    potential_agent.set_state(AgentState.VACCINATED)
                    self.grid.set_agent(potential_agent)
                    self.update_agent_in_registry(potential_agent)
                    return True, 10
                else: 
                    # Agent does not need vaccination
                    return False, -5
        else:
            # No vaccines left
            return False, - 10


    def tick(self):
        ########################################
        # Spread Infection
        #
        # - For all infectious agents, 
        #   infect the neighbouring cells with relevant prob
        #
        # In the first timestep, we avoid infecting agents
        #
        ########################################
        ########################################
        if self.timestep > 0:
            valid_infectious_agents = []
            valid_infectious_agents += self.get_agents_with_state(AgentState.INFECTIOUS)
            valid_infectious_agents += self.get_agents_with_state(AgentState.SYMPTOMATIC)

            for _infectious_agent in valid_infectious_agents:
                target_candidates = self.grid.get_all_neighbours(_infectious_agent.coordinate)
                # print(target_candidates)
                for _target_candidate in target_candidates:
                    if _target_candidate and _target_candidate.state == AgentState.SUSCEPTIBLE:
                        # Add control for "double infections" : 
                        # When two individuals infect the same person at the same time
                        #print("Trying to infect : ", _target_candidate)
                        self.trigger_infection(_target_candidate, prob_infection=self.prob_infection)

        self.tick_agents()

        self.timestep += 1 
        # Update renderer ticks 
        if self.use_renderer:
            self.renderer.update_stats("SIMULATION_TICKS", "{}".format(self.timestep))

        self.env_steps += 1
        if self.renderer:
            self.renderer.update_stats("GAME_TICKS","{}".format(self.env_steps))


    def tick_agents(self):
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



if __name__ == "__main__":
    disease_engine = DiseaseEngine(
                            grid_width=50,
                            grid_height=50,
                            n_agents=1500,
                            n_vaccines=160,
                            initial_infection_fraction=0.1,
                            initial_vaccination_fraction=0.00,
                            prob_infection=0.0,
                            prob_agent_movement=0.00,
                            disease_scheduler="simple_seir",
                            use_renderer=False,
                            toric_grid=True,
                            seed=1001
                            )
    # print(disease_engine.grid)
    # print(disease_engine.grid.get_all_neighbours(Coordinate(0,0)))

    
    for k in range(10):    
        _time = time.time()
        disease_engine.tick()
        print(time.time() - _time)

    while True:
        renderer_actions = disease_engine.update_renderer()
        for _action in renderer_actions:
            print("ACtion : ", _action)
            if _action["type"] == "STEP":
                print("Timestep : {}".format(disease_engine.timestep))
                _time = time.time()
                disease_engine.tick()
                # print(disease_engine.grid)
                print(time.time() - _time)
                print(disease_engine.print_stats())
                print("Observation Shape : ", disease_engine.grid.get_observation().shape)
            elif _action["type"] == "VACCINATE":
                mouse_cell_x = _action["cell_x"]
                mouse_cell_y = _action["cell_y"]
                disease_engine.vaccinate_cell(Coordinate(mouse_cell_x, mouse_cell_y))
            elif _action["type"] == "RUN_TO_COMPLETION":
                while disease_engine.timestep < disease_engine.max_timesteps:
                    disease_engine.tick()
                    renderer_actions = disease_engine.update_renderer()
                print("Final Results : ")
                print(disease_engine.print_stats())
            elif _action["type"] == "RING_VACCINATION":
                _agent_cache = {}
                for _agent_state in disease_engine.agent_registry.keys():
                    if _agent_state in [AgentState.EXPOSED, AgentState.INFECTIOUS, AgentState.SYMPTOMATIC]:
                        for _agent in disease_engine.agent_registry[_agent_state].values():
                            neighbours = disease_engine.grid.get_all_neighbours(_agent.coordinate)
                            for _neighbour in neighbours:
                                """
                                TODO: _neighbour is False in some cases. To be investigated.
                                """
                                if _neighbour and _neighbour.state == AgentState.SUSCEPTIBLE:
                                    disease_engine.vaccinate_cell(Coordinate(_neighbour.coordinate.x, _neighbour.coordinate.y))
                print(disease_engine.print_stats())


        # if disease_engine.timestep >= disease_engine.max_timesteps:
        #     break
        # disease_engine.vaccinate_cell()
        # input()
        # print(disease_engine.agent_registry)
