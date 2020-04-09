#!/usr/bin/env python

"""Tests for `rogi_rl` package."""

import unittest
from rogi_rl import RogiSimEnv


class TestRogiSimEnv(unittest.TestCase):
    """Tests for `rogi_rl` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_env_instantiation(self):
        """
        Test that a newly instantiated env
        returns a valid observation of the correct shape
        """
        config = {
            "width": 50,
            "height": 50
        }
        env = RogiSimEnv(config)
        observation = env.reset()
        assert observation.shape == (50, 50, 6)
