from agent_state import AgentState
import time

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