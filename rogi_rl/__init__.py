"""Top-level package for Rogi RL."""

__author__ = """Sharada Mohanty"""
__email__ = 'spmohanty91@gmail.com'
__version__ = '0.1.0'

from rogi_rl.env import RogiSimEnv  # noqa

from gym.envs.registration import register

register(id='RogiRL-v0',
         entry_point='rogi_rl.env:RogiSimEnv',
         )
