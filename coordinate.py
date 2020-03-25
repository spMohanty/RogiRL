class Coordinate:
    def __init__(self, x=False, y=False):
        self.x = x
        self.y = y

    def __str__(self):
        return "Coordinate(x={} , y={})".format(self.x, self.y)