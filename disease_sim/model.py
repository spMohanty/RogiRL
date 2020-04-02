from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

import numpy as np

try:
    from .agent import DiseaseSimAgent
    from .visualization import CustomTextGrid
    from .disease_planner import SEIRDiseasePlanner
    from .scheduler import CustomScheduler
    from .agent_state import AgentState
    from .vaccination_response import VaccinationResponse
except ImportError:
    from agent import DiseaseSimAgent
    from visualization import CustomTextGrid
    from disease_planner import SEIRDiseasePlanner
    from scheduler import CustomScheduler
    from agent_state import AgentState
    from vaccination_response import VaccinationResponse
    


class DiseaseSimModel(Model):
    """
    The model class holds the model-level attributes, manages the agents, and generally handles
    the global level of our model.

    There is only one model-level parameter: how many agents the model contains. When a new model
    is started, we want it to populate itself with the given number of agents.

    The scheduler is a special model component which controls the order in which agents are activated.
    """

    def __init__(   self, 
                    width=50, 
                    height=50,
                    population_density=0.75,
                    vaccine_density=0,
                    initial_infection_fraction=0.1,
                    initial_vaccination_fraction=0.00,
                    prob_infection=0.2,
                    prob_agent_movement=0.0,
                    disease_planner_config={
                        "latent_period_mu" :  2 * 4,
                        "latent_period_sigma" :  0,
                        "incubation_period_mu" :  5 * 4,
                        "incubation_period_sigma" :  0,
                        "recovery_period_mu" :  14 * 4,
                        "recovery_period_sigma" :  0,
                    },                    
                    max_timesteps=200,
                    toric=True,
                    seed = None
                    ):
        super().__init__()

        self.width = width
        self.height = height
        self.population_density = population_density # fraction of the whole grid that is initiailized with agents 
        self.vaccine_density = vaccine_density # 

        self.n_agents = False
        self.n_vaccines = False

        self.initial_infection_fraction = initial_infection_fraction
        self.initial_vaccination_fraction = initial_vaccination_fraction

        self.prob_infection = prob_infection
        self.prob_agent_movement = prob_agent_movement
        
        self.disease_planner_config = disease_planner_config

        self.max_timesteps = max_timesteps
        self.toric = toric
        self.seed  = seed 

        self.initialize_observation()
        self.initialize_disease_planner()
        self.initialize_scheduler()
        self.initialize_grid()
        self.initialize_agents(
            infection_fraction=self.initial_infection_fraction,
            vaccination_fraction=self.initial_vaccination_fraction
            )
        self.initialize_datacollector()
        self.running = True
        self.datacollector.collect(self)

    ##########################################################################################
    ##########################################################################################
    # Setup Initialization Helper Functions
    ##########################################################################################
    def initialize_observation(self):
        """
        Observation is a nd-array of shape (width, height, num_states)
        where each AgentState will be marked in a separate challenge for each of the cells
        """
        self.observation = np.zeros((self.width, self.height, len(AgentState)))

    def initialize_disease_planner(self):
        """
        Initializes a disease planner that the Agents can use to "schedule" infection progressions
        """
        self.disease_planner = SEIRDiseasePlanner(
                        latent_period_mu = self.disease_planner_config["latent_period_mu"],
                        latent_period_sigma = self.disease_planner_config["latent_period_sigma"],
                        incubation_period_mu = self.disease_planner_config["incubation_period_mu"],
                        incubation_period_sigma = self.disease_planner_config["incubation_period_sigma"],
                        recovery_period_mu = self.disease_planner_config["recovery_period_mu"],
                        recovery_period_sigma = self.disease_planner_config["recovery_period_sigma"]
        )


    def initialize_scheduler(self):
        """
        Initializes the scheduler
        """
        self.schedule = CustomScheduler(self)

    def initialize_grid(self):
        """
        Initializes the initial Grid
        """
        self.grid = SingleGrid(width=self.width, height=self.height, torus=self.toric)

    def initialize_agents(self, infection_fraction, vaccination_fraction):
        """
        Intializes the intial agents on the grid
        """
        assert 0 < self.population_density <= 1, \
            "population_density should be between (0, 1]"
        
        # Assess the actual population
        self.n_agents = int(self.width * self.height * self.population_density)
        # Assess the available number of vaccines
        self.n_vaccines = int(self.n_agents * self.vaccine_density)
        

        # Assess the number of agents that have to be infected (the seed infection)
        number_of_agents_to_infect = int(infection_fraction * self.n_agents)
        number_of_agents_to_vaccinate = int(vaccination_fraction * self.n_agents)

        # Assess the maximum number of vaccines available in the whole simulation
        self.max_vaccines = self.n_vaccines + number_of_agents_to_vaccinate

        for i in range(self.n_agents):
            agent = DiseaseSimAgent(
                            unique_id = i, 
                            model = self, 
                            prob_agent_movement = self.prob_agent_movement
                        )
            self.schedule.add(agent)
            self.grid.position_agent(agent, x="random", y="random")

            # Update model observation
            # TODO- This has to be refactored to avoid repitition
            agent_x, agent_y = agent.pos
            self.observation[agent_x, agent_y, agent.state.value] = 1

            # Seed the infection in a fraction of the agents
            if i < number_of_agents_to_infect:
                agent.trigger_infection(prob_infection=1.0)
            
            # Seed the vaccination in a fraction of the agents
            if i >= number_of_agents_to_infect and i < (number_of_agents_to_infect + number_of_agents_to_vaccinate):
                agent.set_state(AgentState.VACCINATED)

    def initialize_datacollector(self):
        """
        Setup the initial datacollector
        """
        self.datacollector = DataCollector(
            model_reporters = {
                    "Susceptible" : lambda m: m.get_population_fraction_by_state(AgentState.SUSCEPTIBLE),
                    "Exposed" : lambda m: m.get_population_fraction_by_state(AgentState.EXPOSED),
                    "Infectious" : lambda m: m.get_population_fraction_by_state(AgentState.INFECTIOUS),
                    "Symptomatic" : lambda m: m.get_population_fraction_by_state(AgentState.SYMPTOMATIC),
                    "Recovered" : lambda m: m.get_population_fraction_by_state(AgentState.RECOVERED),
                    "Vaccinated" : lambda m: m.get_population_fraction_by_state(AgentState.VACCINATED)
                }
        )

    ##########################################################################################
    ##########################################################################################
    # State Aggregation
    #       - Functions for easy access/aggregation of simulation wide state
    ##########################################################################################

    def get_observation(self):
        # assert self.observation.sum(axis=-1).max() <= 1.0
        # Assertion disabled for perf reasons
        return self.observation

    def get_population_fraction_by_state(self, state: AgentState):
        return self.schedule.get_agent_fraction_by_state(state)

    def is_running(self):
        return self.running

    ##########################################################################################
    ##########################################################################################
    # Actions
    #        - Functions for actions that can be performed on the model
    ##########################################################################################

    def step(self):
        """
        A model step. Used for collecting data and advancing the schedule
        """
        self.propagate_infections()
        self.datacollector.collect(self)
        self.schedule.step()

    def vaccinate_cell(self, cell_x, cell_y):
        """
        Vaccinates an agent at cell_x, cell_y, if present

        Response with :
        (is_vaccination_successful: boolean, vaccination_response: VaccinationResponse)
        """
        
        # Case 0 : No vaccines left
        if self.n_vaccines <= 0:
            return False, VaccinationResponse.AGENT_VACCINES_EXHAUSTED
        self.n_vaccines -= 1

        # Case 1 : Cell is empty
        if self.grid.is_cell_empty((cell_x, cell_y)):
            return False, VaccinationResponse.CELL_EMPTY

        agent = self.grid[cell_x][cell_y]
        if agent.state == AgentState.SUSCEPTIBLE:
            # Case 2 : Agent is susceptible, and can be vaccinated
            agent.set_state(AgentState.VACCINATED)
            return True, VaccinationResponse.VACCINATION_SUCCESS
        elif agent.state == AgentState.EXPOSED:
            # Case 3 : Agent is already exposed, and its a waste of vaccination
            return False, VaccinationResponse.AGENT_EXPOSED
        elif agent.state == AgentState.INFECTIOUS:
            # Case 4 : Agent is already infectious, and its a waste of vaccination
            return False, VaccinationResponse.AGENT_INFECTIOUS
        elif agent.state == AgentState.SYMPTOMATIC:
            # Case 5 : Agent is already Symptomatic, and its a waste of vaccination
            return False, VaccinationResponse.AGENT_SYMPTOMATIC
        elif agent.state == AgentState.RECOVERED:
            # Case 6 : Agent is already Recovered, and its a waste of vaccination
            return False, VaccinationResponse.AGENT_RECOVERED
        elif agent.state == AgentState.VACCINATED:
            # Case 7 : Agent is already Vaccination, and its a waste of vaccination
            return False, VaccinationResponse.AGENT_VACCINATED
        raise NotImplementedError()

    ##########################################################################################
    ##########################################################################################
    # Misc
    ##########################################################################################

    def check_if_simulation_is_complete(self):
        """
        Simulation is complete if 
        """
        return not self.running

    def tick(self):
        """
        a mirror function for the internal step function 
        to help avoid confusion in the RL codebases (with the RL step)
        """
        self.step()

    def propagate_infections(self):
        """
        Propagates infection during a single simulation step
        """
        valid_infectious_agents = []
        valid_infectious_agents += self.schedule.get_agents_by_state(AgentState.INFECTIOUS)
        valid_infectious_agents += self.schedule.get_agents_by_state(AgentState.SYMPTOMATIC)

        for _infectious_agent in valid_infectious_agents:
            target_candidates = self.grid.get_neighbors(
                pos = _infectious_agent.pos,
                moore = True, 
                include_center = False,
                radius = 1
            )
            for _target_candidate in target_candidates:
                if _target_candidate.state == AgentState.SUSCEPTIBLE:
                    _target_candidate.trigger_infection(prob_infection=self.prob_infection)


if __name__ == "__main__":
    model = DiseaseSimModel(
                    width=50,
                    height=50,
                    population_density=0.75,
                    vaccine_density=0.0,
                    initial_infection_fraction=0.1,
                    initial_vaccination_fraction=0.0,
                    prob_infection=1.0,
                    prob_agent_movement=0.0,
                    disease_planner_config={
                        "latent_period_mu" :  2 * 4,
                        "latent_period_sigma" :  0,
                        "incubation_period_mu" :  5 * 4,
                        "incubation_period_sigma" :  0,
                        "recovery_period_mu" :  14 * 4,
                        "recovery_period_sigma" :  0,
                    },                    
                    max_timesteps=200,
                    toric=True)
    
    import time
    import numpy as np
    per_step_times = []
    for k in range(100):
        _time = time.time()
        model.step()
        per_step_times.append(time.time() - _time)
        _obs = model.get_observation()
        # print(model.get_population_fraction_by_state(AgentState.SUSCEPTIBLE))

        # Random Vaccinations
        # random_x = model.random.choice(range(50))
        # random_y = model.random.choice(range(50))
        # print(model.vaccinate_cell(random_x, random_y))

        # print(per_step_times[-1])
        # print(model.datacollector.get_model_vars_dataframe())
        # print("S", model.schedule.get_agent_count_by_state(AgentState.SUSCEPTIBLE))
        # print("E", model.schedule.get_agent_count_by_state(AgentState.EXPOSED))
        # print("I", model.schedule.get_agent_count_by_state(AgentState.INFECTIOUS))
        # print("R", model.schedule.get_agent_count_by_state(AgentState.RECOVERED))
        # print(viz.render())
    per_step_times = np.array(per_step_times)
    print("Per Step Time : {} += {}", per_step_times.mean(), per_step_times.std())


        