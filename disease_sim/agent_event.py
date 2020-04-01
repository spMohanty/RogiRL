
try:
    from .agent_state import AgentState
except ImportError:
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
        self.mark_as_pending()
        self.created_at = time.time()
        self.updated_at = time.time()
    
    def mark_as_executed(self):
        """
        Mark that this event has been executed
        """
        self.execution_status = True
        self.updated_at = time.time()

    def mark_as_pending(self):
        """
        Mark that the execution of this event is pending
        """
        self.execution_status = False

    def __str__(self):
        return "AgentEvent(t = {} || {} => {} || Status : {})".format(
            self.update_timestep,
            self.previous_state.name,
            self.new_state.name,
            self.execution_status
        )
    def __repr__(self):
        return self.__str__()