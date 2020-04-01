from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

try:
    from .agent import DiseaseSimAgent
    from .visualization import CustomTextGrid
    from .disease_planner import SimpleSEIRDiseasePlanner, SEIRDiseasePlanner
except ImportError:
    from agent import DiseaseSimAgent
    from visualization import CustomTextGrid
    from disease_planner import SimpleSEIRDiseasePlanner, SEIRDiseasePlanner

class DiseaseSimModel(Model):
    """
    The model class holds the model-level attributes, manages the agents, and generally handles
    the global level of our model.

    There is only one model-level parameter: how many agents the model contains. When a new model
    is started, we want it to populate itself with the given number of agents.

    The scheduler is a special model component which controls the order in which agents are activated.
    """

    def __init__(   self, 
                    width=3, 
                    height=3,
                    n_agents=1,
                    n_vaccines=100,
                    initial_infection_fraction=0.2,
                    initial_vaccination_fraction=0.05,
                    prob_infection=0.2,
                    prob_agent_movement=0.1,
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
        
        self.schedule = RandomActivation(self)
        self.initialize_disease_planner(disease_planner=disease_planner)

        self.grid = SingleGrid(width=width, height=height, torus=self.toric)

        assert self.n_agents <= self.width * self.height, \
            "More number of agents requested than the actual space available"

        for i in range(self.n_agents):
            agent = DiseaseSimAgent(
                            unique_id = i, 
                            model = self, 
                            prob_agent_movement = self.prob_agent_movement
                        )
            self.schedule.add(agent)
            self.grid.position_agent(agent, x="random", y="random")

            # Seed the infection in a fraction of the agents
            if self.random.random() < self.initial_infection_fraction:
                agent.trigger_infection(prob_infection=1.0)

        # example data collector
        self.datacollector = DataCollector(
            # model_reporters = {"rand" : lambda x : self.random.random()}
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


    def step(self):
        """
        A model step. Used for collecting data and advancing the schedule
        """
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
                    prob_infection=0.2,
                    prob_agent_movement=0.0,
                    disease_scheduler="simple_seir",
                    max_timesteps=200,
                    toric=True)

    
    viz = CustomTextGrid(model.grid)
    # print(viz.render())

    import time
    for k in range(10):
        _time = time.time()
        model.step()
        print(time.time() - _time)
        # print(model.datacollector.get_model_vars_dataframe())
        # print(viz.render())


        