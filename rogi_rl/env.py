import gym
from gym import spaces
from gym.utils import seeding

from enum import Enum
import numpy as np


from rogi_rl.agent_state import AgentState
from rogi_rl.model import DiseaseSimModel
from rogi_rl.vaccination_response import VaccinationResponse


class ActionType(Enum):
    STEP = 0
    VACCINATE = 1


class RogiSimEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, config={}):
        # Setup Config
        self.default_config = dict(
                    width=50,
                    height=50,
                    population_density=0.75,
                    vaccine_density=0.05,
                    initial_infection_fraction=0.1,
                    initial_vaccination_fraction=0.05,
                    prob_infection=0.2,
                    prob_agent_movement=0.0,
                    disease_planner_config={
                        "latent_period_mu": 2 * 4,
                        "latent_period_sigma": 0,
                        "incubation_period_mu": 5 * 4,
                        "incubation_period_sigma": 0,
                        "recovery_period_mu": 14 * 4,
                        "recovery_period_sigma": 0,
                    },
                    max_simulation_timesteps=200,
                    early_stopping_patience=14,
                    use_renderer=False,
                    toric=True,
                    dummy_simulation=False,
                    debug=False)
        self.config = {}
        self.config.update(self.default_config)
        self.config.update(config)

        self.dummy_simulation = self.config["dummy_simulation"]
        self.debug = self.config["debug"]

        self.width = self.config["width"]
        self.height = self.config["height"]

        self.use_renderer = self.config["use_renderer"]

        self.action_space = spaces.MultiDiscrete(
            [
                len(ActionType), self.width, self.height
            ])
        self.observation_space = spaces.Box(
                                    low=np.float32(0),
                                    high=np.float32(1),
                                    shape=(
                                        self.width,
                                        self.height,
                                        len(AgentState)))

        self._model = None
        self.running_score = None
        self.np_random = np.random

        self.renderer = False

        self.viewer = None

        if self.use_renderer:
            self.initialize_renderer()

        self.reward = 0

    def reset(self):
        # Delete Model if already exists
        if self._model:
            del self._model

        if self.dummy_simulation:
            """
            In dummy simulation mode
            return a randomly sampled observation
            """
            return self.observation_space.sample()

        width = self.config['width']
        height = self.config['height']
        population_density = self.config['population_density']
        vaccine_density = self.config['vaccine_density']
        initial_infection_fraction = self.config['initial_infection_fraction']
        initial_vaccination_fraction = \
            self.config['initial_vaccination_fraction']
        prob_infection = self.config['prob_infection']
        prob_agent_movement = self.config['prob_agent_movement']
        disease_planner_config = self.config['disease_planner_config']
        max_simulation_timesteps = self.config['max_simulation_timesteps']
        early_stopping_patience = \
            self.config['early_stopping_patience']
        toric = self.config['toric']

        """
        Seeding Strategy :
            - The env maintains a custom seed/unsseded np.random instance
            accessible at self.np_random

            whenever env.seed() is called, the said np_random instance
            is seeded

            and during every new instantiation of a DiseaseEngine instance,
            it is seeded with a random number sampled from the self.np_random.
        """
        _simulator_instance_seed = self.np_random.rand()
        # Instantiate Disease Model
        self._model = DiseaseSimModel(
            width, height,
            population_density, vaccine_density,
            initial_infection_fraction, initial_vaccination_fraction,
            prob_infection, prob_agent_movement,
            disease_planner_config,
            max_simulation_timesteps, early_stopping_patience,
            toric, seed=_simulator_instance_seed
        )

        # Set the max timesteps of an env as the sum of :
        # - max_simulation_timesteps
        # - Number of Vaccines available

        self._max_episode_steps = self.config['max_simulation_timesteps'] + \
            self._model.n_vaccines

        # Tick model
        self._model.tick()

        """
        """
        self.running_score = self.get_current_game_score()
        # return observation
        return self._model.get_observation()

    def initialize_renderer(self):

        from rogi_rl.renderer import Renderer

        self.renderer = Renderer(
                grid_size=(self.width, self.height)
            )
        self.renderer.setup()

    def update_renderer(self, mode='human'):
        """
        Updates the latest board state on the renderer
        """
        if mode == "human":
            # Draw Renderer
            # Update Renderer State
            model = self._model
            scheduler = model.get_scheduler()
            total_agents = scheduler.get_agent_count()
            state_metrics = self.get_current_game_metrics()

            initial_vaccines = int(
                model.initial_vaccination_fraction * model.n_agents)

            _vaccines_given = \
                model.max_vaccines - model.n_vaccines - initial_vaccines

            _unused_vaccine_ratio = model.n_vaccines/(
                _vaccines_given + model.n_vaccines)

            _simulation_steps = int(scheduler.steps)

            # Game Steps includes steps in which each agent is vaccinated
            _game_steps = _simulation_steps + _vaccines_given

            self.renderer.update_stats("SCORE", "{:.3f}".format(self.reward))
            self.renderer.update_stats("VACCINE_BUDGET", "{}".format(
                model.n_vaccines))
            self.renderer.update_stats("SIMULATION_TICKS", "{}".format(
                _simulation_steps))
            self.renderer.update_stats("GAME_TICKS", "{}".format(_game_steps))

            self.renderer.update_stats("UNUSED_VACCINE_RATIO",
                                       "{:.2f}".format(_unused_vaccine_ratio))

            for _state in AgentState:
                key = f"population.{_state.name}"
                stats = state_metrics[key]
                self.renderer.update_stats(
                    key,
                    "{} ({:.2f}%)".format(
                        int(stats * total_agents),
                        stats*100
                    )
                )
                color = self.renderer.COLOR_MAP.get_color(_state)
                agents = scheduler.get_agents_by_state(_state)
                for _agent in agents:
                    _agent_x, _agent_y = _agent.pos
                    self.renderer.draw_cell(
                                _agent_x, _agent_y,
                                color
                            )

            # Update the rest of the renderer
            self.renderer.pre_render()
            self.renderer.post_render()
            return True

        return False

    def get_current_game_score(self):
        """
        Returns the current game score

        The game score is currently represented as :
            (percentage of susceptibles left in the population)
        """
        return self._model.get_population_fraction_by_state(
                AgentState.SUSCEPTIBLE
            )

    def get_current_game_metrics(self, dummy_simulation=False):
        """
        Returns a dictionary containing important game metrics
        """
        _d = {}
        # current population fraction of different states
        for _state in AgentState:
            if not dummy_simulation:
                _value = self._model.get_population_fraction_by_state(_state)
            else:
                _value = self.np_random.rand()
            _d[f"population.{_state.name}"] = _value
        # Add R0 to the game metrics
        _d["R0/10"] = self._model.contact_network.compute_R0()/10.0

        # Add UNUSED VACCINE RATIO to the game metrics
        model = self._model

        initial_vaccines = int(
                model.initial_vaccination_fraction * model.n_agents)

        _unused_vaccine_ratio = model.n_vaccines/(
                model.max_vaccines - initial_vaccines)

        _d['UNUSED_VACCINE_RATIO'] = _unused_vaccine_ratio

        return _d

    def step(self, action):
        # Handle dummy_simulation Mode
        if self.dummy_simulation:
            return self.dummy_env_step()

        assert self.action_space.contains(
            action), "%r (%s) invalid" % (action, type(action))
        if self._model is None:
            raise Exception("env.step() called before calling env.reset()")

        action = [int(x) for x in action]
        if self.debug:
            print("Action : ", action)

        # Handle action propagation in real simulator
        action_type = action[0]
        cell_x = action[1]
        cell_y = action[2]

        _observation = False
        _done = False
        _info = {}
        if action_type == ActionType.STEP.value:
            self._model.tick()
            _observation = self._model.get_observation()
        elif action_type == ActionType.VACCINATE.value:
            vaccination_success, response = \
                self._model.vaccinate_cell(cell_x, cell_y)
            _observation = self._model.get_observation()

            # Force Run simulation to completion if
            # run out of vaccines
            if response == VaccinationResponse.AGENT_VACCINES_EXHAUSTED:
                while self._model.is_running():
                    self._model.tick()
                    _observation = self._model.get_observation()

        # Compute difference in game score
        current_score = self.get_current_game_score()
        _step_reward = current_score - self.running_score
        self.reward = _step_reward
        self.running_score = current_score

        # Add custom game metrics to info key
        game_metrics = self.get_current_game_metrics()
        for _key in game_metrics.keys():
            _info[_key] = game_metrics[_key]

        _done = not self._model.is_running()
        return _observation, _step_reward, _done, _info

    def dummy_env_step(self):
        """
        Implements a fake env.step for faster Integration Testing
        with RL experiments framework
        """
        observation = self.observation_space.sample()
        reward = self.np_random.rand()
        done = True if self.np_random.rand() < 0.01 else False
        info = {}
        game_metrics = self.get_current_game_metrics(dummy_simulation=True)
        info.update(game_metrics)

        return observation, reward, done, info

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def render(self, mode='human', close=False):
        """
        This methods provides the option to render the
        environment's behavior to a window which should be
        readable to the human eye if mode is set to 'human'.
        """
        if not self.use_renderer:
            return

        if not self.renderer:
            self.initialize_renderer()

        self.update_renderer(mode=mode)

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None


if __name__ == "__main__":

    env_config = dict(
                    width=50,
                    height=50,
                    population_density=0.75,
                    vaccine_density=0.05,
                    initial_infection_fraction=0.1,
                    initial_vaccination_fraction=0.05,
                    prob_infection=0.2,
                    prob_agent_movement=0.0,
                    disease_planner_config={
                        "latent_period_mu":  2 * 4,
                        "latent_period_sigma":  0,
                        "incubation_period_mu":  5 * 4,
                        "incubation_period_sigma":  0,
                        "recovery_period_mu":  14 * 4,
                        "recovery_period_sigma":  0,
                    },
                    max_simulation_timesteps=200,
                    early_stopping_patience=14,
                    use_renderer=False,
                    toric=True,
                    dummy_simulation=False,
                    debug=True)
    env = RogiSimEnv(config=env_config)
    print("USE RENDERER ?", env.use_renderer)
    observation = env.reset()
    done = False
    k = 0
    while not done:
        observation, reward, done, info = env.step(env.action_space.sample())
        k += 1
        # print(observation.shape)
        # print(k, reward, done)
    # print(observation.shape())
