from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

try:
    from .agent import DiseaseSimAgent
    from .visualization import CustomTextGrid
    from .disease_planner import SimpleSEIRDiseasePlanner, SEIRDiseasePlanner
    from .scheduler import CustomScheduler
    from .agent_state import AgentState
except ImportError:
    from agent import DiseaseSimAgent
    from visualization import CustomTextGrid
    from disease_planner import SimpleSEIRDiseasePlanner, SEIRDiseasePlanner
    from scheduler import CustomScheduler
    from agent_state import AgentState
    


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
                    n_agents=1000,
                    n_vaccines=100,
                    initial_infection_fraction=0.5,
                    initial_vaccination_fraction=0.05,
                    prob_infection=0.2,
                    prob_agent_movement=0.0,
                    disease_planner="simple_seir",
                    max_timesteps=200,
                    toric=True,
                    seed = None
                    ):
        super().__init__()

        self.width = width
        self.height = height
        self.n_agents = n_agents
        self.n_vaccines = n_vaccines

        self.initial_infection_fraction = initial_infection_fraction
        self.initial_vaccination_fraction = initial_vaccination_fraction

        self.prob_infection = prob_infection
        self.prob_agent_movement = prob_agent_movement

        self.max_timesteps = max_timesteps
        self.toric = toric
        self.seed  = seed 

        self.schedule = CustomScheduler(self)
        self.initialize_disease_planner(disease_planner=disease_planner)

        self.grid = SingleGrid(width=width, height=height, torus=self.toric)

        assert self.n_agents <= self.width * self.height, \
            "More number of agents requested than the actual space available"


        number_of_agents_to_infect = int(self.initial_infection_fraction * self.n_agents)
        for i in range(self.n_agents):
            agent = DiseaseSimAgent(
                            unique_id = i, 
                            model = self, 
                            prob_agent_movement = self.prob_agent_movement
                        )
            self.schedule.add(agent)
            self.grid.position_agent(agent, x="random", y="random")

            # Seed the infection in a fraction of the agents
            if i < number_of_agents_to_infect:
                agent.trigger_infection(prob_infection=1.0)

        # example data collector
        self.datacollector = DataCollector(
            model_reporters = {
                    "susceptible_frac" : lambda m: m.schedule.get_agent_fraction_by_state(AgentState.SUSCEPTIBLE),
                    "exposed_frac" : lambda m: m.schedule.get_agent_fraction_by_state(AgentState.EXPOSED),
                    "infectious_frac" : lambda m: m.schedule.get_agent_fraction_by_state(AgentState.INFECTIOUS),
                    "recovered_frac" : lambda m: m.schedule.get_agent_fraction_by_state(AgentState.RECOVERED),
                }
        )

        self.running = True
        self.datacollector.collect(self)

    def initialize_disease_planner(self, disease_planner="simple_seir"):
        if disease_planner == "simple_seir":
            self.disease_planner = \
                SimpleSEIRDiseasePlanner(random=self.random)
        elif disease_planner == "seir":
            self.disease_planner = \
                SEIRDiseasePlanner(random=self.random)
        else:
            raise NotImplementedError()

    
    def propagate_infections(self):
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


    def step(self):
        """
        A model step. Used for collecting data and advancing the schedule
        """
        self.propagate_infections()
        self.datacollector.collect(self)
        self.schedule.step()

if __name__ == "__main__":
    model = DiseaseSimModel(
                    width=50,
                    height=50,
                    n_agents=1000,
                    n_vaccines=100,
                    initial_infection_fraction=0.2,
                    initial_vaccination_fraction=0.05,
                    prob_infection=1.0,
                    prob_agent_movement=0.0,
                    disease_planner="simple_seir",
                    max_timesteps=200,
                    toric=True)

    
    viz = CustomTextGrid(model.grid)
    # print(viz.render())
    
    import time
    for k in range(100):
        _time = time.time()
        model.step()
        print(time.time() - _time)
        # print(model.datacollector.get_model_vars_dataframe())
        # print("S", model.schedule.get_agent_count_by_state(AgentState.SUSCEPTIBLE))
        # print("E", model.schedule.get_agent_count_by_state(AgentState.EXPOSED))
        # print("I", model.schedule.get_agent_count_by_state(AgentState.INFECTIOUS))
        # print("R", model.schedule.get_agent_count_by_state(AgentState.RECOVERED))
        # print(viz.render())


        