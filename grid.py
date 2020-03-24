#!/usr/bin/env python

import numpy as np

from individual import Individual, IndividualStates

class Grid:
    def __init__(
                    self,
                    grid_width = 100,
                    grid_height = 100,
                    number_of_agents = 100
                ):
        
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.number_of_agents = number_of_agents

        self.initialize_grid()
    
    def initialize_grid(self):
        self.grid = []

        for _height in range(self.grid_height):
            self.grid.append([False]*self.grid_width)


    def render_grid(self, mode="ascii"):

        # ASCII mode
        print("  " + "_ "*self.grid_width)
        for _y in range(self.grid_height):
            print("| ", end="")
            for _x in range(self.grid_width):
                # Case of empty grid
                if self.grid[_x][_y] == False:
                    print(".", end=" ")
            print("|")
        print("  " + "_ "*self.grid_width)
    
if __name__ == "__main__":
    grid = Grid(20, 20, 20)
    grid.render_grid()