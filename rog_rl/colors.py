from rog_rl.agent_state import AgentState
import colorama


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
    LIGHT_GREY = (234, 237, 237)
    BLUE_GREY = (84, 110, 122)


class ANSI_COLOR_MAP:
    FORE_BLACK = colorama.Fore.BLACK
    FORE_RED = colorama.Fore.RED
    FORE_GREEN = colorama.Fore.GREEN
    FORE_YELLOW = colorama.Fore.YELLOW
    FORE_BLUE = colorama.Fore.BLUE
    FORE_MAGENTA = colorama.Fore.MAGENTA
    FORE_CYAN = colorama.Fore.CYAN
    FORE_WHITE = colorama.Fore.WHITE
    FORE_RESET = colorama.Fore.RESET

    BACK_BLACK = colorama.Back.BLACK
    BACK_RED = colorama.Back.RED
    BACK_GREEN = colorama.Back.GREEN
    BACK_YELLOW = colorama.Back.YELLOW
    BACK_BLUE = colorama.Back.BLUE
    BACK_MAGENTA = colorama.Back.MAGENTA
    BACK_CYAN = colorama.Back.CYAN
    BACK_WHITE = colorama.Back.WHITE
    BACK_RESET = colorama.Back.RESET


class ColorMap:
    def __init__(self, mode="rgb"):
        """
        Params:
            mode : "rgb" or "ansi"
        """
        assert mode in ["rgb", "ansi"]

        if mode == "rgb":
            self.COLORS = Colors()
        elif mode == "ansi":
            self.ANSI_COLORS = ANSI_COLOR_MAP()

        self.COLOR_MAP = {}
        # AgentState Colors
        for _state in AgentState:
            if mode == "rgb":
                """
                Prepare the RGB ColorMap
                """
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

                self.COLOR_MAP["R0/10"] = self.COLORS.BLUE_GREY
                self.COLOR_MAP["BACKGROUND_COLOR"] = self.COLORS.WHITE
                self.COLOR_MAP["AGENT_STATE_TEXT_COLOR"] = self.COLORS.GREY

            elif mode == "ansi":
                """
                Prepare the Colorama Colormap
                """
                if _state == AgentState.SUSCEPTIBLE:
                    self.COLOR_MAP[_state] = self.ANSI_COLORS.FORE_GREEN
                elif _state == AgentState.EXPOSED:
                    self.COLOR_MAP[_state] = self.ANSI_COLORS.FORE_CYAN
                elif _state == AgentState.INFECTIOUS:
                    self.COLOR_MAP[_state] = self.ANSI_COLORS.FORE_MAGENTA  # noqa
                elif _state == AgentState.SYMPTOMATIC:
                    self.COLOR_MAP[_state] = self.ANSI_COLORS.FORE_RED
                elif _state == AgentState.RECOVERED:
                    self.COLOR_MAP[_state] = self.ANSI_COLORS.FORE_BLUE
                elif _state == AgentState.VACCINATED:
                    self.COLOR_MAP[_state] = self.ANSI_COLORS.FORE_YELLOW

                self.COLOR_MAP["R0/10"] = self.ANSI_COLORS.BACK_CYAN
                self.COLOR_MAP["BACKGROUND_COLOR"] = self.ANSI_COLORS.FORE_WHITE  # noqa
                self.COLOR_MAP["AGENT_STATE_TEXT_COLOR"] = self.ANSI_COLORS.FORE_WHITE  # noqa

                self.COLOR_MAP["BACK_RESET"] = self.ANSI_COLORS.BACK_RESET
                self.COLOR_MAP["FORE_RESET"] = self.ANSI_COLORS.FORE_RESET

    def get_color(self, d):
        try:
            return self.COLOR_MAP[d]
        except KeyError:
            raise NotImplementedError(
                    "Unknown key in ColorMap. Was it initialized ?")


if __name__ == "__main__":
    colors = Colors()
    # TODO setup a small pygame setup to display all the colors in the palette
