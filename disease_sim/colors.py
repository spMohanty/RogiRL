try:
    from .agent_state import AgentState
except ImportError:
    from agent_state import AgentState

class Colors:
    """
    Reference : https://materialuicolors.co/
    # Level : 600

    Can potentially use : https://github.com/secretBiology/SecretColors/
    """
    WHITE = (255, 255, 255)
    RED = (229, 57, 53)
    PINK = (216, 27, 96)
    PURPLE = (142, 36, 170)
    DEEP_PURPLE = (94, 53, 177)
    INDIGO = (57, 73, 171)
    BLUE = (30, 136, 229)
    LIGHT_BLUE = (3, 155, 229)
    CYAN = (0, 172, 193)
    TEAL = (0, 137, 123)
    GREEN = (67, 160, 71)
    LIGHT_GREEN = (124, 179, 66)
    LIME = (192, 202, 51)
    YELLOW = (253, 216, 53)
    AMBER = (255, 179, 0)
    ORANGE = (251, 140, 0)
    DEEP_ORANGE = (244, 81, 30)
    BROWN = (109, 76, 65)
    GREY = (117, 117, 117)
    LIGHT_GREY = ( 234, 237, 237 )
    BLUE_GREY = (84, 110, 122)

class ColorMap:
    def __init__(self):
        self.COLORS = Colors()
        self.COLOR_MAP = {}

        # AgentState Colors
        for _state in AgentState:
            if _state == AgentState.SUSCEPTIBLE:
                self.COLOR_MAP[_state] = self.COLORS.GREEN
            elif _state == AgentState.EXPOSED:
                self.COLOR_MAP[_state] = self.COLORS.PURPLE
            elif _state == AgentState.INFECTIOUS:
                self.COLOR_MAP[_state] = self.COLORS.BROWN
            elif _state == AgentState.SYMPTOMATIC:
                self.COLOR_MAP[_state] = self.COLORS.RED
            elif _state == AgentState.RECOVERED:
                self.COLOR_MAP[_state] = self.COLORS.BLUE
            elif _state == AgentState.VACCINATED:
                self.COLOR_MAP[_state] = self.COLORS.YELLOW
        
        self.COLOR_MAP["BACKGROUND_COLOR"] = self.COLORS.WHITE
        self.COLOR_MAP["AGENT_STATE_TEXT_COLOR"] = self.COLORS.GREY

    def get_color(self, d):
        try:
            return self.COLOR_MAP[d]
        except KeyError:
                raise NotImplementedError("Unknown key in ColorMap. Was it initialized ?")



if __name__ == "__main__":
    colors = Colors()
    # TODO setup a small pygame setup to display all the colors in the palette


