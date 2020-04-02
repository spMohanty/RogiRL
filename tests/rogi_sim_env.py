import unittest

from rogi_rl import rogi_rl
from rogi_rl import cli

from rogi_rl import RogiSimEnv

class TestRogiSimEnv(unittest.TestCase):
    """Tests for `rogi_rl` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_env_instantiation(self):
        """Test something."""
        env = RogiSimEnv()
        observation = env.reset()
        assert False, "Whoops !"

