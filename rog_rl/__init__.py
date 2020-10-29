"""Top-level package for Rog RL."""

__author__ = """Sharada Mohanty"""
__email__ = 'spmohanty91@gmail.com'
__version__ = '0.1.0'

from rog_rl.env import RogSimEnv  # noqa

from gym.envs.registration import register

register(id='RogRL-v0',
         entry_point='rog_rl.env:RogSimEnv',
         )
