from mesa import Agent
try:
    from .agent_state import AgentState
except ImportError:
    from agent_state import AgentState

class DiseaseSimAgent(Agent):  # noqa
    """
    DiseaseSimAgent
    """
    pos = None
    moore = True
    prob_agent_movement = 0.0

    def __init__(self, unique_id, model,  prob_agent_movement=0.0, moore=True):
        """
        Customize the agent
        """
        self.unique_id = unique_id
        super().__init__(unique_id, model)

        self._is_infection_scheduled = False
        self.prob_agent_movement = prob_agent_movement
        self.moore = moore

        # self.state = self.random.choice([x for x in AgentState])
        self.state = AgentState.SUSCEPTIBLE
        self.state_transition_plan = {} # Holds the state transition plan, with timestep as the key

    def step(self):
        self.random_move()
        self.process_state_transitions()
    
    def process_state_transitions(self):
        try:
            _event = self.state_transition_plan[self.model.schedule.steps]
            assert self.state == _event.previous_state, "Mismatch in state during state_transition"
            self.state = _event.new_state

            self.model.schedule.update_agent_state_in_registry(self, _event.previous_state)
            _event.mark_as_executed()
        except KeyError:
            """
            If not state transition plan exists for the said timestep
            then ignore
            """
            pass

    def trigger_infection(self, prob_infection=1.0):
        if self._is_infection_scheduled:
            return
        else:
            if self.random.random() < prob_infection:
                # Prepare a disease plan
                disease_plan = \
                    self.model.disease_planner.get_disease_plan(base_timestep=self.model.schedule.steps)
                for _agent_event in disease_plan:
                    # Check if a state transition plan is already present for the said timestep
                    try:
                        foo = self.state_transition_plan[_agent_event.update_timestep]
                        raise Exception("Attempt to assign multiple state transition plans for the same timestep")
                    except KeyError:
                        pass
                    # Mark the state transition plan for the said timestep
                    self.state_transition_plan[_agent_event.update_timestep] = _agent_event
                self._is_infection_scheduled = True

    def random_move(self):        
        if self.random.random() < self.prob_agent_movement:
            # Find empty cells in neighborhood
            empty_cells_in_neighborhood = []            
            for x,y in self.model.grid.iter_neighborhood(
                pos = self.pos, moore = self.moore, include_center = False, radius = 1):
                if (x,y) in self.model.grid.empties:
                    empty_cells_in_neighborhood.append((x,y))
            # If empty cells are availabel - move to a randomly chosen one
            if len(empty_cells_in_neighborhood) > 0:
                new_position = self.random.choice(empty_cells_in_neighborhood)
                # Move to a randomly selected empty cell in the neighborhood

                # Update global observation vector
                self.model.observation[self.pos[0], self.pos[1], : ] = 0
                self.model.grid.move_agent(self, new_position)
                self.model.observation[self.pos[0], self.pos[1], self.state.value ] = 1


        
        
