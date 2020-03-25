#!/usr/bin/env python



import numpy as np
from enum import Enum
import uuid
import time

# Susceptible, Exposed, Infectious, Symptomatic, Recovered/Dead
class AgentState(Enum):
    SUSCEPTIBLE = 0
    EXPOSED = 1
    INFECTIOUS = 2
    SYMPTOMATIC = 3
    RECOVERED = 4
    DEAD = 5

class Coordinate:
    def __init__(self, x=False, y=False):
        self.x = x
        self.y = y

    def __str__(self):
        return "Coordinate(x={} , y={})".format(self.x, self.y)

class AgentEvent:
    def __init__(   self, 
                    previous_state=AgentState.SUSCEPTIBLE,
                    new_state=AgentState.SUSCEPTIBLE,
                    update_timestep=-1
                ):
        self.previous_state = previous_state
        self.new_state = new_state
        self.update_timestep = update_timestep
        self.wall_time = time.time()

    def __str__(self):
        return "AgentEvent({} => {} || t = {} || wall_time = {})".format(
            self.previous_state.name,
            self.new_state.name,
            self.update_timestep,
            self.wall_time
        )
    def __repr__(self):
        return self.__str__()

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
    

