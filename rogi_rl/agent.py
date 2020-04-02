from mesa import Agent
from rogi_rl.agent_state import AgentState

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
        self.state_transition_plan = {} # Holds the state transition plan, with timestep as the key
        
        # Default State for Agents
        self.state = AgentState.SUSCEPTIBLE

    def step(self):
        self.random_move()
        self.process_state_transitions()

    def set_state(self, new_state:AgentState):
        previous_state = self.state
        self.state = new_state

        # Update Agent State Registry in Scheduler
        self.model.schedule.update_agent_state_in_registry(self, previous_state=previous_state)

        # Update Global Observation in model observation buffer
        self.model.observation[self.pos[0], self.pos[1], : ] = 0
        self.model.observation[self.pos[0], self.pos[1], self.state.value ] = 1

    
    def process_state_transitions(self):
        try:
            _event = self.state_transition_plan[self.model.schedule.steps]
            assert self.state == _event.previous_state, "Mismatch in state during state_transition"
            self.set_state(_event.new_state)
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

    def move_to(self, new_position):
        """
        Move the agent to a new location on the grid
        and do other associated house keeping tasks
            - Update global observation in model
        """
        # Clear up global observation cache in model at the previous coord
        self.model.observation[self.pos[0], self.pos[1], : ] = 0
        # Move Agent in Grid
        self.model.grid.move_agent(self, new_position)
        # Add a new entry in the global observation cache for the new position
        self.model.observation[self.pos[0], self.pos[1], self.state.value ] = 1

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

                self.move_to(new_position)


        
        
