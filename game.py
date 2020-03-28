#!/usr/bin/env python

import pygame
from enum import Enum
from colors import Colors
import random
import numpy as np

pygame.init()
######################################################
######################################################
# COLORS
COLORS = Colors()


######################################################
######################################################
# Constants
WIDTH = 1024
HEIGHT = 768
CONTROL_PANEL_WIDTH = 200
PADDING_TOP = 10

GRID_WIDTH = WIDTH - CONTROL_PANEL_WIDTH

CELL_WIDTH = 16
CELL_HEIGHT = 16

CIRCLE_PADDING = 3 

## Initializing 
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Width, Height

def draw_grid(screen, grid_size=(5,5), base_x=0, base_y=0):
    MAX_X = base_x + grid_size[0] * CELL_WIDTH
    MAX_Y = base_y + grid_size[1] * CELL_HEIGHT
    
    # Draw Vertical ticks
    for _x_coord in range(grid_size[0]+1):
        _x_val = base_x + CELL_WIDTH * _x_coord
        start_loc = (_x_val, base_y)
        end_loc = (_x_val, MAX_Y)
        pygame.draw.line(screen, COLORS.LIGHT_GREY, start_loc, end_loc)

    # Draw Vertical ticks
    for _y_coord in range(grid_size[1]+1):
        _y_val = base_y + CELL_HEIGHT * _y_coord
        start_loc = (base_x, _y_val)
        end_loc = (MAX_X, _y_val)
        pygame.draw.line(screen, COLORS.LIGHT_GREY, start_loc, end_loc)


def draw_circle(grid_x, grid_y, color=COLORS.RED, base_coord=(0, 0)):

    grid_y += 1

    cell_base_x = base_coord[0] + grid_x * CELL_WIDTH
    cell_base_y = base_coord[1] + grid_y * CELL_HEIGHT

    circle_center = [int(cell_base_x + CELL_WIDTH/2), int(cell_base_y + CELL_HEIGHT/2)]
    circle_radius = int((CELL_WIDTH - 2 * CIRCLE_PADDING) / 2)

    pygame.draw.circle(screen, color, circle_center, circle_radius)
    


while True:
    #######################################################
    # Event Loop
    for event in pygame.event.get():
        if event.type in [pygame.QUIT] :
            pygame.quit()
            quit()
    #######################################################
    # Game Logic
    screen.fill(COLORS.WHITE)

    # pygame.draw.circle(screen, COLORS.BLUE, [50, 20], 10)
    # Draw Grid

    grid_size = (30, 30)
    # draw_grid(screen, grid_size, base_x=CONTROL_PANEL_WIDTH, base_y=PADDING_TOP)


    # VALID_COLORS = [COLORS.WHITE,COLORS.RED,COLORS.PINK,COLORS.PURPLE,COLORS.DEEP_PURPLE,COLORS.INDIGO,COLORS.BLUE,COLORS.LIGHT_BLUE,COLORS.CYAN,COLORS.TEAL,COLORS.GREEN,COLORS.LIGHT_GREEN,COLORS.LIME,COLORS.YELLOW,COLORS.AMBER,COLORS.ORANGE,COLORS.DEEP_ORANGE,COLORS.BROWN,COLORS.GREY,COLORS.LIGHT_GREY,COLORS.BLUE_GREY]

    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            if np.random.rand() < 1:
                draw_circle(x, y, color = COLORS.BLUE, base_coord=(CONTROL_PANEL_WIDTH, 0))

    pygame.display.update() #update()


