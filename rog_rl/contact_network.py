#!/usr/bin/env python
import numpy as np


class ContactNetwork:
    """
    This keeps a record of all the "contacts" that happen in a
    single simulation
    """
    def __init__(self):
        self.contact_network = {}
        self.infection_network = {}
        self.infection_counter = {}

    def register_contact(self, agent_a, agent_b):
        raise NotImplementedError()

    def register_infection_spread(self, agent_a, agent_b):
        """
        Register the fact that agent_a infected agent_b
        """
        agent_a_id = agent_a.unique_id
        agent_b_id = agent_b.unique_id

        try:
            self.infection_network[agent_a_id]
        except KeyError:
            self.infection_network[agent_a_id] = set()
            self.infection_counter[agent_a_id] = 0

        self.infection_network[agent_a_id].add(agent_b_id)
        self.infection_counter[agent_a_id] += 1

    def compute_R0(self):
        """
        Returns the value of R0 based on all
        the registered infections
        """
        if len(self.infection_counter.keys()) == 0:
            return 0
        # TODO- This can be optimized by computing a running mean
        return np.array(list(self.infection_counter.values())).mean()
