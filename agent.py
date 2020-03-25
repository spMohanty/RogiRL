#!/usr/bin/env python



import numpy as np
import uuid
from agent_event import AgentEvent
from agent_state import AgentState
from coordinate import Coordinate


class Agent:
    def __init__(
                self,
                coordinate : Coordinate,
                state:AgentState = AgentState.SUSCEPTIBLE,
                uid=False
                ):
        self.coordinate = coordinate
        self.state = state
        self.uid = uid
        if not self.uid:
            self.uid = str(uuid.uuid4())[:5]
        assert type(self.uid) == str
        self.event_log = []
        self.timestep = 0

    def add_event(self, event: AgentEvent):
        self.event_log.append(event)

    def tick(self):
        """
            - house keeping calls for each time tick
            - can optionally be passed a function (From the disease engine), which can modify its attributes if necessary 
        """
        pass

    def set_state(self, state: AgentState):
        """
        - Sets the current state of the agent
        - does validations about certain state transitions
        - does internal housekeeping of any other metadata that needs to be captured
        """
        # TODO : Add validation 
        event = AgentEvent(
            previous_state = self.state,
            new_state = state,
            update_timestep = self.timestep
        )
        self.add_event(event)
        self.state = state

    def move_to(self, coord: Coordinate):
        """
            - Moves the agent to a particular coordinate
        """
        self.coordinate = coord
    
    def __str__(self):
        return "Agent(state={}, coord=({}, {}), timestep={}, id={})".format(self.state.name, self.coordinate.x, self.coordinate.y, self.timestep, self.uid)

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":

    coordinate = Coordinate(0,0)
    print(coordinate)

    agent = Agent(coordinate, AgentState.SUSCEPTIBLE)
    print(agent)

    coordinate = Coordinate(100,100)
    agent.move_to(coordinate)

    print(agent)
    print(agent.event_log)
    agent.set_state(AgentState.INFECTIOUS)
    print(agent)
    print(agent.event_log)
    

