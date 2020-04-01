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

        self.state = self.random.choice([x for x in AgentState])

    def step(self):
        self.random_move()

        
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
                self.model.grid.move_agent(self, new_position)


        
        
