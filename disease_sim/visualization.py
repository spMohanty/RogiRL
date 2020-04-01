from mesa.visualization.TextVisualization import TextGrid

def _default_converter(agent):
    if agent == None:
        return "-\t"
    else:
        return "*\t"

class CustomTextGrid(TextGrid):
    grid = None

    def __init__(self, grid, converter=None):
        """ Create a new ASCII grid visualization.
        Args:
            grid: The underlying Grid object.
            converter: function for converting the content of each cell
                       to ascii. Takes the contents of a cell, and returns
                       a single character.
        """
        self.grid = grid
        if converter:
            self.converter = converter
        else:
            self.converter = _default_converter

    def render(self, endl="\n"):
        """ What to show when printed. """
        viz = ""
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                c = self.grid[y][x]
                viz += self.converter(c)
            viz += endl
        return viz