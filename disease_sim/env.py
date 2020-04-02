import gym
from gym import error, spaces, utils
from gym.utils import seeding

from enum import Enum
import numpy as np

try:
    from .agent_state import AgentState
    from .model import DiseaseSimModel
except ImportError:
    from agent_state import AgentState
    from model import DiseaseSimModel


class ActionType(Enum):
    STEP = 0
    VACCINATE = 1

class DiseaseSimEnv(gym.Env):
    metadata = {'render.modes': ['human']}
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
                    debug=True
                    ):
        self.width = width
        self.height = height
        self.n_agents = n_agents
        self.n_vaccines = n_vaccines

        self.initial_infection_fraction = initial_infection_fraction
        self.initial_vaccination_fraction = initial_vaccination_fraction

        self.prob_infection = prob_infection
        self.prob_agent_movement = prob_agent_movement

        self.disease_planner = disease_planner

        self.max_timesteps = max_timesteps
        self.toric = toric
        self.debug = debug

        self.action_space = spaces.MultiDiscrete(
            [
                len(ActionType), self.width, self.height
            ])
        self.observation_space = spaces.Box(low=0, high=1, shape=(
            self.width, self.height, len(AgentState)
        ))

        self._model = None
        self.np_random = np.random


    def step(self, action):
        assert self.action_space.contains(action), "Invalid action provided !"
        action = [int(x) for x in action]
        if self.debug:
            print(action)
        
        action_type = action[0]
        cell_x = action[1]
        cell_y = action[2]

        _observation = False
        _reward = 0.0
        _done = False
        _info = {}
        if action_type == ActionType.STEP.value:
            self._model.tick()
            _observation = self._model.get_observation()
            reward = 0.0
            _done = self._model.running            
        elif action_type == ActionType.VACCINATE.value:
            vaccination_success, response = self._model.vaccinate_cell(cell_x, cell_y)
            _observation = self._model.get_observation()
            _done = self._model.running

        _done = self._model.running 
        return _observation, _reward, _done, _info



    def reset(  self,
                width=None, 
                height=None,
                n_agents=None,
                n_vaccines=None,
                initial_infection_fraction=None,
                initial_vaccination_fraction=None,
                prob_infection=None,
                prob_agent_movement=None,
                disease_planner=None,
                max_timesteps=None,
                toric=None):

        # Delete Model if already exists
        if self._model:
            del self._model

        # Replace reset parameters with default parameters if they are not provided
        if width == None: width = self.width
        if height == None: height = self.height
        if n_agents == None: n_agents = self.n_agents
        if n_vaccines == None: n_vaccines = self.n_vaccines
        if initial_infection_fraction == None: initial_infection_fraction = self.initial_infection_fraction
        if initial_vaccination_fraction == None: initial_vaccination_fraction = self.initial_vaccination_fraction
        if prob_infection == None: prob_infection = self.prob_infection
        if prob_agent_movement == None: prob_agent_movement = self.prob_agent_movement
        if disease_planner == None: disease_planner = self.disease_planner
        if max_timesteps == None: max_timesteps = self.max_timesteps
        if toric == None: toric = self.toric

        """
        Seeding Strategy :
            - The env maintains a custom seed/unsseded np.random instance
            accessible at self.np_random

            whenever env.seed() is called, the said np_random instance is seeded

            and during every new instantiation of a DiseaseEngine instance, it is seeded
            with a random number sampled from the self.np_random. 
        """
        _simulator_instance_seed = self.np_random.rand()
        # Instantiate Disease Model
        self._model = DiseaseSimModel(
            width, height, 
            n_agents, n_vaccines,
            initial_infection_fraction, initial_vaccination_fraction,
            prob_infection, prob_agent_movement,
            disease_planner, 
            max_timesteps, 
            toric, seed = _simulator_instance_seed
        )

        # Tick model
        self._model.tick()
        # return observation
        return self._model.get_observation()


    def seed(self, seed=None):
        self.np_random.seed(seed)


    def render(self, mode='human', close=False):
        """
        This methods provides the option to render the environment's behavior to a window 
        which should be readable to the human eye if mode is set to 'human'.
        """
        pass



if __name__ == "__main__":

    env = DiseaseSimEnv(
            width=4, height=4,
            n_agents=2,
            prob_agent_movement=0,
            debug=True
            )
    observation = env.reset()
    for k in range(10):
        observation, reward, done, info = env.step(env.action_space.sample())
        print("Step : ", k)
        print(observation.shape, observation.sum(axis=-1))
        print(reward, done)
    # print(observation.shape())