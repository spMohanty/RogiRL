#!/usr/bin/env python

from mesa import Agent, Model
from mesa.time import RandomActivation
try:
    from .agent_state import AgentState
except ImportError:
    from agent_state import AgentState


class CustomScheduler(RandomActivation):
    def __init__(self, model: Model) -> None:
        super().__init__(model)

        self._agent_state_index = {}
        for state in AgentState:
            self._agent_state_index[state] = {}

    def add(self, agent: Agent) -> None:
        self._agents[agent.unique_id] = agent
        self._agent_state_index[agent.state][agent.unique_id] = agent
    
    def remove(self, agent: Agent) -> None:
        del self._agents[agent.unique_id]

        for state in AgentState:
            try:
                del self._agent_state_index[state][agent.unique_id]
            except KeyError:
                pass
    
    def update_agent_state_in_registry(self, agent: Agent, previous_state: AgentState) -> None:
        del self._agent_state_index[previous_state][agent.unique_id]
        self._agent_state_index[agent.state][agent.unique_id] = agent

        ## Update the Model Observation 
        # self.model.observation[agent.pos]
        agent_x, agent_y = agent.pos
        self.model.observation[agent_x, agent_y, previous_state.value] = 0
        self.model.observation[agent_x, agent_y, agent.state.value] = 1

    def get_agents_by_state(self, state: AgentState):
        return list(self._agent_state_index[state].values())

    def get_agent_count_by_state(self, state: AgentState) -> int:
        """ Returns the current number of agents in a particular state. """
        return len(self._agent_state_index[state].keys())

    def get_agent_fraction_by_state(self, state: AgentState) -> int:
        """ Returns the current number of agents in a particular state. """
        return len(self._agent_state_index[state].keys()) / self.get_agent_count()    