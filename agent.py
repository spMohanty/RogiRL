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
        self.event_buffer = {}
        self.timestep = 0

    def register_event(self, event: AgentEvent):
        timestep_of_event = event.update_timestep
        assert timestep_of_event >= self.timestep, "Event from the past added to event_buffer"

        # Initialize an empty array for the timestep 
        # if it doesnt exist already
        try:
            foo = self.event_buffer[timestep_of_event]
        except KeyError:
            self.event_buffer[timestep_of_event] = []
        
        # Add the event to the list of events supposed to be 
        # executed at the said timestep
        self.event_buffer[timestep_of_event].append(
            event
        )

    def tick(self):
        """
            - house keeping calls for each time tick

            - Check if there are any Events that are pending to be executed for this timestep
            - Increase the timestep count
        """
        try:
            pending_events = self.event_buffer[self.timestep]
            for _event in pending_events:
                assert self.state == _event.previous_state, "Mismatch in state during AgentEvent execution"
                self.set_state(_event.new_state)
                _event.mark_as_executed()
        except KeyError:
            # There are no events available for this timestep
            pass

        self.timestep += 1

    def set_state(self, state: AgentState):
        """
        - Sets the current state of the agent
        - does validations about certain state transitions
        - Any other associated housekeeping tasks
        """
        # TODO : Add validation 
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
    print(agent.event_buffer)
    agent.set_state(AgentState.INFECTIOUS)
    
    _event = AgentEvent(update_timestep=100)
    agent.register_event(_event)
    print(agent)
    print(agent.event_buffer)
    

