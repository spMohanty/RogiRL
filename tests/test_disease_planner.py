#!/usr/bin/env python

"""
Tests the disease_planner class
"""
import pytest
from rog_rl.disease_planner import SEIRDiseasePlanner

import numpy as np


def tests_sanity_of_parameters_provided():
    """
        Ensures that the parameters
        provided for disease progression period models
        are sensible.
    """

    for k in range(1000):
        latent_period_mu = np.random.randint(0, 100)
        incubation_period_mu = np.random.randint(0, 100)
        recovery_period_mu = np.random.randint(0, 100)
        latent_period_sigma = 0
        incubation_period_sigma = 0
        recovery_period_sigma = 0

        variables_list = \
            [latent_period_mu, incubation_period_mu, recovery_period_mu]
        if not(variables_list == sorted(variables_list)):
            """
            An exception should be raised whenever we dont meet the criteria
            of :
                Latent Period < Incubation Period < Recover Period
            """
            with pytest.raises(Exception):
                SEIRDiseasePlanner(
                    latent_period_mu=latent_period_mu,
                    latent_period_sigma=latent_period_sigma,
                    incubation_period_mu=incubation_period_mu,
                    incubation_period_sigma=incubation_period_sigma,  # noqa
                    recovery_period_mu=recovery_period_mu,
                    recovery_period_sigma=recovery_period_sigma,
                    random=False
                )


def tests_zero_sigma_gives_constant_values():
    """
    This tests that passing in 0 as sigma value for the
    different parameters ensure we get constant values
    for the individual periods
    """

    for k in range(1000):

        latent_period_mu = np.random.randint(1, 100)
        incubation_period_mu = latent_period_mu + np.random.randint(1, 100)
        recovery_period_mu = \
            incubation_period_mu + np.random.randint(1, 100)

        latent_period_sigma = 0
        incubation_period_sigma = 0
        recovery_period_sigma = 0

        disease_planner = SEIRDiseasePlanner(
            latent_period_mu=latent_period_mu,
            latent_period_sigma=latent_period_sigma,
            incubation_period_mu=incubation_period_mu,
            incubation_period_sigma=incubation_period_sigma,
            recovery_period_mu=recovery_period_mu,
            recovery_period_sigma=recovery_period_sigma,
            random=False
        )

        latent_period, incubation_period, recovery_period = \
            disease_planner.sample_disease_progression()

        assert latent_period == latent_period_mu
        assert incubation_period == incubation_period_mu
        assert recovery_period == recovery_period_mu
