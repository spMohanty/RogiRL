import numpy as np

from agent import Agent
from agent_event import AgentEvent
from agent_state import AgentState
from coordinate import Coordinate

class Grid:
    def __init__(self, width=100, height=100, n_agents=100, toric=True, np_random=False):
        self.width = width
        self.height = height
        self.n_agents = n_agents
        self.toric = toric

        # Initialize grid
        self.grid = {}

        self.grid_state = np.zeros((self.width, self.height, len(AgentState)))

        # # Intialize grid state
        # number_of_agent_states = len(AgentState)
        # self.grid_state = np.zeros((width, height, number_of_agent_states))

        # Initialize Agent Registry
        # self.agent_registry = {
        #     "agent_id" : {},
        #     "agent_state" : {}
        # }
        # for _state in AgentState:
        #     self.agent_registry["agent_state"][_state] = {}

        self.np_random = np_random
        if not self.np_random:
            self.np_random = np.random

    def get_agent(self, coord: Coordinate):
        """
        Returns the agent at a location, else False
        """
        try:
            if self.toric:
                coord.x %= self.width
                coord.y %= self.height

            return self.grid[hash(coord)]
        except KeyError:
            return False

    def clear_cell(self, coord: Coordinate):
        try:
            del self.grid[hash(coord)]
            self.grid_state[coord.x,coord.y,:] = 0
        except KeyError:
            pass

    def set_agent(self, agent:Agent):
        """
        Sets the location of the agent at a particular coordinate

        Updates associated registries, etc

        If previous entries for the agent exist, this function should 
        cleanly deal with the same
        """

        ## Check if agent is already on the grid
        # try:
        #     _agent = self.agent_registry["agent_id"][agent.id]
        # except KeyError:
        #     # Agent is not in the registry
        #     pass
        if self.toric:
            agent.coordinate.x %= self.width
            agent.coordinate.y %= self.height

        self.grid[hash(agent.coordinate)] = agent
        self.grid_state[agent.coordinate.x,agent.coordinate.y,int(agent.state.value)] = 1

    def get_observation(self):
        return self.grid_state

    def get_random_empty_cells(self, n_cells=1):
        """
        Returns random empty cell in the whole grid 

        If no empty cells available, it returns False
        """
        # iteration = 0
        # while True:
        #     random_coord = Coordinate(
        #                         self.np_random.randint(self.width),
        #                         self.np_random.randint(self.height),
        #                     )
        #     try:
        #         foo = self.grid[random_coord]
        #     except KeyError:
        #         return random_coord
            
        #     iteration += 1

        #     if iteration >= 10:
        #         print("[WARNING] Random Empty Cell not found in {} iterations. Giving Up".format(iteration))
        #         return False
        # TODO : Make this more efficient later
        empty_cells = []
        for x in range(self.width):
            for y in range(self.height):
                _agent = self.get_agent(Coordinate(x,y))
                if _agent == False:
                    # Empty cell
                    empty_cells.append(Coordinate(x,y))
        
        if len(empty_cells) == 0:
            return False
        else:
            self.np_random.shuffle(empty_cells)
            return empty_cells[:n_cells]

    def get_random_empty_neighbouring_cell(self, coord: Coordinate, radius=1):
        """
        Returns a random empty neighbouring cell for a particular coord

        if no empty cells available, it returns False
        """
        empty_cells = []
        for _x_diff in range(-1*radius, radius+1):
            for _y_diff in range(-1*radius, radius+1):
                if _x_diff == 0 and _y_diff == 0:
                    # This is the case of the coord-cell
                    continue
                
                target_coord = Coordinate(coord.x + _x_diff, coord.y + _y_diff)
                agent_at_coord = self.get_agent(target_coord)
                if not agent_at_coord:
                    empty_cells.append(target_coord)

        if len(empty_cells) == 0:
            return False
        else: 
            return self.np_random.choice(empty_cells)

    def get_all_neighbours(self, coord: Coordinate, radius=1):
        """
        Returns all neighbouring agents in a particular view radius
        """
        neighbours = []
        for _x_diff in range(-1*radius, radius+1):
            for _y_diff in range(-1*radius, radius+1):                
                target_coord = Coordinate(coord.x + _x_diff, coord.y + _y_diff)
                # print("Target Coord : ", target_coord)
                # print(self.get_agent(target_coord))
                try:
                    foo = self.get_agent(target_coord)
                    # an agent exists at this location
                    neighbours.append(self.get_agent(target_coord))
                except KeyError:
                    # Empty Cell ! Ignore
                    pass

        return neighbours

    def __str__(self):
        render_string = ""
        for _y in range(self.height):
            render_string += "| " 
            for _x in range(self.width):
                cell_item = self.get_agent(Coordinate(_x, _y))
                if cell_item == False:
                    # Case of empty cell
                    render_string += "- "
                elif type(cell_item) == Agent:
                    # Case of an actual agent in the cell
                    if cell_item.state == AgentState.SUSCEPTIBLE:
                        render_string += "* "
                    elif cell_item.state == AgentState.EXPOSED:
                        render_string += "o "
                    elif cell_item.state == AgentState.INFECTIOUS:
                        render_string += "O "
                    elif cell_item.state == AgentState.RECOVERED:
                        render_string += "R "
                    elif cell_item.state == AgentState.SYMPTOMATIC:
                        render_string += "O "
                    elif cell_item.state == AgentState.VACCINATED:
                        render_string += "V "
                    else:
                        raise NotImplementedError("Unknown Agent State encountered.")
            
            render_string += "|\n"
        render_string += "  " + "_ "*self.width + "\n"
        return render_string
    
    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    grid = Grid(width=10, height=10, n_agents=10)
    print(grid)

    _agent = Agent(Coordinate(15,115))
    _agent.set_state(AgentState.SUSCEPTIBLE)

    grid.set_agent(_agent)

    print(grid)
    print(grid.grid)

    _c = Coordinate(5,5)
    print(grid.get_agent(_c))

    ## Initialize random agents
    grid = Grid(width=10, height=10, n_agents=10)
    for i in range(10):
        empty_cell = grid.get_random_empty_cells()
        _agent = Agent(empty_cell)

        state = np.random.choice(AgentState)
        _agent.set_state(state)

        grid.set_agent(_agent)

        print(grid)