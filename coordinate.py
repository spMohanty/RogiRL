class Coordinate:
    def __init__(self, x=False, y=False):
        self.x = x
        self.y = y

    def __str__(self):
        return "Coordinate(x={} , y={})".format(self.x, self.y)
    
    def __repr__(self):
        return "{}_{}".format(self.x,self.y)

    def __hash__(self):
        # This assumes that the the max values for x and y are in the range 0,10**5
        return (self.x * 10**5) + self.y