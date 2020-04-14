from rogi_rl import RogiSimEnv  # noqa
from rogi_rl import env as environ
from rogi_rl.agent_state import AgentState
from gym import wrappers
import pytest
import gym
import numpy as np
import time

"""Tests for `rogi_rl` gym based env."""


@pytest.mark.parametrize('name, width, height, toric, dummy_simulation, \
                         use_renderer', [
    ('RogiRL-v0', 10, 10, False, False, "ascii"),
    ('RogiRL-v0', 20, 20, True, False, "human"),
    ('RogiRL-v0', 30, 30, True, False, False),
    ('RogiRL-v0', 40, 40, False, False, False),
])
def test_env_instantiation(name, width, height, toric, dummy_simulation,
                           use_renderer):
    """
    Test that standard gym env actions
    methods like reset, step
    """
    seed = 1
    n_states = len(AgentState)
    n_action_types = len(environ.ActionType)

    # Renderer is disabled for now but it can be enabled
    # To run different renders, comment below line
    use_renderer = False

    env_config = dict(
        width=width,
        height=height,
        toric=toric,
        dummy_simulation=dummy_simulation,
        use_renderer=use_renderer,
        debug=True,
        np_random=seed
    )
    env = gym.make(name, config=env_config)
    np.random.seed(seed)
    # env = RogiSimEnv(config=env_config)
    observation = env.reset()
    assert observation.shape == (width, height, n_states)
    reward_history = [env._model.get_population_fraction_by_state(
        AgentState.SUSCEPTIBLE
    )]
    step_rewards = []
    for i in range(n_action_types):
        action = env.action_space.sample()
        # Ensure we do both step and vaccinate
        action[0] = i
        state, reward, done, info = env.step(action)
        reward_history.append(env._model.get_population_fraction_by_state(
            AgentState.SUSCEPTIBLE))

        assert isinstance(state, np.ndarray)
        assert state.shape == (width, height, n_states)
        assert isinstance(reward, float)
        _cur_step_reward = reward_history[-1] - reward_history[-2]
        step_rewards.append(_cur_step_reward)
        assert round(reward, 3) == round(_cur_step_reward, 3)
        assert round(env.cumulative_reward, 3) == round(sum(step_rewards), 3)
        assert isinstance(done, bool)
        assert isinstance(info, dict)
        assert len(info) == len(env.get_current_game_metrics(dummy_simulation))
        if use_renderer:
            env.render(use_renderer)
            time.sleep(0.01)
    env.close()


def test_make():
    name = 'RogiRL-v0'
    env = gym.make(name)
    assert env.spec.id == name
    assert isinstance(env, gym.Env)


def test_monitor():
    name = 'RogiRL-v0'
    env = gym.make(name)
    env = wrappers.Monitor(env, "recording", force=True)
    assert env.spec.id == name
    assert isinstance(env, wrappers.Monitor)
