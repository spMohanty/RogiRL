#!/usr/bin/env python

import pygame
import numpy as np
import time

from colors import Colors, ColorMap
from agent_state import AgentState

class Renderer:
    def __init__(self, grid_size=(30,30)):
        self.grid_size = grid_size

        self.COLORS = Colors()
        self.COLOR_MAP = ColorMap()
        self.setup_constants()
        self.setup_stats()

    def setup_constants(self):

        self.AGENT_STATUS_FONT_SIZE = 18
        self.AGENT_STATUS_LINE_SPACE = 5

        self.CONTROL_PANEL_WIDTH = 200
        self.TOP_PANEL_HEIGHT = 20
        self.MARGIN = 5
        
        # CELL_PROPERTIES
        self.CELL_WIDTH = 16
        self.CELL_HEIGHT = 16
        self.CELL_PADDING =  3

        self.MOUSE_HIGHLIGHTER_WIDTH = 3

        # GRID_PROPERTIES
        self.GRID_BASE_X = self.MARGIN \
            + self.CONTROL_PANEL_WIDTH \
            + 2 * self.MARGIN
        self.GRID_BASE_Y = self.MARGIN + self.TOP_PANEL_HEIGHT

        self.GRID_MAX_X = self.GRID_BASE_X + \
            (self.CELL_WIDTH) * self.get_grid_width()
        self.GRID_MAX_Y = self.GRID_BASE_Y + \
            (self.CELL_HEIGHT) * self.get_grid_height()

        self.WIDTH = self.GRID_MAX_X + self.MARGIN
        self.HEIGHT = self.GRID_MAX_Y + self.MARGIN
    
    def setup_stats(self):
        self.stats = {}

        # AgentState Values
        for _state in AgentState:
            self.stats[_state] = 0

        # Simulation Progress 
        self.stats["SIMULATION_TICKS"] = 0
        # Game Progress 
        self.stats["GAME_TICKS"] = 0
        self.stats["VACCINE_BUDGET"] = 0


        self.WIDTH = self.GRID_MAX_X + self.MARGIN 
        self.HEIGHT = self.GRID_MAX_Y + self.MARGIN + (len(self.stats.keys()) * (self.AGENT_STATUS_LINE_SPACE + self.AGENT_STATUS_FONT_SIZE ))



    def get_cell_base(self, cell_x, cell_y):
        return (
            self.GRID_BASE_X + cell_x * self.CELL_WIDTH,
            self.GRID_BASE_Y + cell_y * self.CELL_HEIGHT,
        )

    def get_grid_width(self): return self.grid_size[0]
    def get_grid_height(self): return self.grid_size[1]

    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def draw_stats(self):
        font = pygame.font.SysFont("consolas", self.AGENT_STATUS_FONT_SIZE)
        top_x = self.MARGIN
        top_y = self.GRID_BASE_Y + self.MARGIN

        ################################################################
        ################################################################
        # Simulation Statistics Header
        _text_string = "Simulation Statistics"
        heading_font = pygame.font.SysFont("consolas", int(self.AGENT_STATUS_FONT_SIZE + 2))
        _text = heading_font.render(_text_string, True, 
                    self.COLOR_MAP.get_color("AGENT_STATE_TEXT_COLOR"),
                    self.COLOR_MAP.get_color("BACKGROUND_COLOR"))
        self.screen.blit(_text, (top_x, top_y))
        top_y += self.AGENT_STATUS_LINE_SPACE + self.AGENT_STATUS_FONT_SIZE
        ################################################################
        ################################################################
        # Line
        ################################################################
        rect_base_x = top_x
        rect_base_y = top_y

        rect_width = self.CONTROL_PANEL_WIDTH
        rect_height = 2

        pygame.draw.rect(self.screen, self.COLOR_MAP.get_color("AGENT_STATE_TEXT_COLOR"), (
            rect_base_x, rect_base_y,
            rect_width, rect_height
        ))

        top_y +=  2 * rect_height + self.AGENT_STATUS_LINE_SPACE
        ################################################################
        ################################################################
        # Render AgentState Values
        ################################################################
        for _state in AgentState:
            _text_string = str(self.stats[_state])
            _text_string += " "
            _text_string += _state.name
            _text = font.render(_text_string, True, 
                        self.COLOR_MAP.get_color(_state),
                        self.COLOR_MAP.get_color("BACKGROUND_COLOR"))
            self.screen.blit(_text, (top_x, top_y))

            top_y += self.AGENT_STATUS_LINE_SPACE + self.AGENT_STATUS_FONT_SIZE
        ################################################################
        ################################################################
        # Line
        ################################################################
        rect_base_x = top_x
        rect_base_y = top_y

        rect_width = self.CONTROL_PANEL_WIDTH
        rect_height = 2

        pygame.draw.rect(self.screen, self.COLOR_MAP.get_color("AGENT_STATE_TEXT_COLOR"), (
            rect_base_x, rect_base_y,
            rect_width, rect_height
        ))

        top_y +=  2 * rect_height + self.AGENT_STATUS_LINE_SPACE
        ################################################################
        ################################################################
        # Simulation Progress Header
        _text_string = "Progress"
        heading_font = pygame.font.SysFont("consolas", int(self.AGENT_STATUS_FONT_SIZE + 2))
        _text = heading_font.render(_text_string, True, 
                    self.COLOR_MAP.get_color("AGENT_STATE_TEXT_COLOR"),
                    self.COLOR_MAP.get_color("BACKGROUND_COLOR"))
        self.screen.blit(_text, (top_x, top_y))
        top_y += self.AGENT_STATUS_LINE_SPACE + self.AGENT_STATUS_FONT_SIZE
        ################################################################
        ################################################################
        # Line
        ################################################################
        rect_base_x = top_x
        rect_base_y = top_y

        rect_width = self.CONTROL_PANEL_WIDTH
        rect_height = 2

        pygame.draw.rect(self.screen, self.COLOR_MAP.get_color("AGENT_STATE_TEXT_COLOR"), (
            rect_base_x, rect_base_y,
            rect_width, rect_height
        ))

        top_y +=  2 * rect_height + self.AGENT_STATUS_LINE_SPACE
        for _state in ["SIMULATION_TICKS", "GAME_TICKS", "VACCINE_BUDGET"]:
            _text_string = str(self.stats[_state])
            _text_string += " "
            _text_string += _state
            _text = font.render(_text_string, True, 
                        self.COLOR_MAP.get_color("AGENT_STATE_TEXT_COLOR"),
                        self.COLOR_MAP.get_color("BACKGROUND_COLOR"))
            self.screen.blit(_text, (top_x, top_y))

            top_y += self.AGENT_STATUS_LINE_SPACE + self.AGENT_STATUS_FONT_SIZE
        

    def update_stats(self, key, value):
        if type(value) != str:
            raise Exception("rendere.stats value is not String")
        self.stats[key] = value
        #print(self.stats)
            

    def draw_grid(self):
        # Draw Vertical Ticks
        for _x_coord in range(self.get_grid_width()+1):
            cell_base = self.get_cell_base(_x_coord, 0)
            start_coord = (
                cell_base[0],
                self.GRID_BASE_Y
            )
            end_coord = (
                cell_base[0],
                self.GRID_MAX_Y
            )
            pygame.draw.line(
                self.screen, 
                self.COLORS.LIGHT_GREY, 
                start_coord, end_coord)

        # Draw Horizontal Ticks
        for _y_coord in range(self.get_grid_height()+1):
            cell_base = self.get_cell_base(0, _y_coord)
            start_coord = (
                self.GRID_BASE_X,
                cell_base[1]
            )
            end_coord = (
                self.GRID_MAX_X,
                cell_base[1]
            )
            pygame.draw.line(
                self.screen, 
                self.COLORS.LIGHT_GREY, 
                start_coord, end_coord)

    def draw_cell(self, cell_x, cell_y, color=False):
        cell_base = self.get_cell_base(cell_x, cell_y)

        if not color:
            color = self.COLORS.BLUE

        rect_base_x = cell_base[0] + self.CELL_PADDING
        rect_base_y = cell_base[1] + self.CELL_PADDING

        rect_width = self.CELL_WIDTH - 2*self.CELL_PADDING
        rect_height = self.CELL_HEIGHT - 2*self.CELL_PADDING

        pygame.draw.rect(self.screen, color, (
            rect_base_x, rect_base_y,
            rect_width, rect_height
        ))

    def get_mouse_cell(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x > self.GRID_BASE_X and mouse_x <= self.GRID_MAX_X:
            if mouse_y > self.GRID_BASE_Y and mouse_y <= self.GRID_MAX_Y:
                mouse_x -= self.GRID_BASE_X
                mouse_y -= self.GRID_BASE_Y
            
                mouse_cell_x = int(mouse_x / self.CELL_WIDTH)
                mouse_cell_y = int(mouse_y / self.CELL_HEIGHT)

                return (mouse_cell_x, mouse_cell_y)
        return False

    def draw_mouse_hightlight(self):
        mouse_cell = self.get_mouse_cell()
        if mouse_cell:
            mouse_cell_x, mouse_cell_y = mouse_cell

            mouse_cell_base = self.get_cell_base(mouse_cell_x, mouse_cell_y)

            # Draw left line
            pygame.draw.rect(self.screen, self.COLORS.YELLOW,
                (mouse_cell_base[0], 
                mouse_cell_base[1],
                self.MOUSE_HIGHLIGHTER_WIDTH, self.CELL_HEIGHT)
            )
            # Draw Top line
            pygame.draw.rect(self.screen, self.COLORS.YELLOW,
                (mouse_cell_base[0], 
                mouse_cell_base[1],
                self.CELL_WIDTH, self.MOUSE_HIGHLIGHTER_WIDTH)
            )
            # Draw Right Line
            pygame.draw.rect(self.screen, self.COLORS.YELLOW,
                (mouse_cell_base[0] + self.CELL_WIDTH - self.MOUSE_HIGHLIGHTER_WIDTH, 
                mouse_cell_base[1],
                self.MOUSE_HIGHLIGHTER_WIDTH, self.CELL_HEIGHT)
            )
            # Draw Bottom Line
            pygame.draw.rect(self.screen, self.COLORS.YELLOW,
                (mouse_cell_base[0], 
                mouse_cell_base[1] + self.CELL_HEIGHT - self.MOUSE_HIGHLIGHTER_WIDTH,
                self.CELL_WIDTH, self.MOUSE_HIGHLIGHTER_WIDTH)
            )


    def command_handler(self):
        """
        Comands Handled : 
            - QUIT
            - VACCINATE
                - Mouse Click
            - STEP
                - "Space" button
        """
        ACTIONS = []
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                ACTIONS.append({
                    "type" : "QUIT"
                })
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_SPACE:
                    ACTIONS.append({
                        "type" : "STEP",
                    })
                elif event.key == pygame.K_r:
                    ACTIONS.append({
                        "type" : "RUN_TO_COMPLETION"
                    })
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_cell = self.get_mouse_cell()
                if mouse_cell: # If the interaction has happened within the grid
                    mouse_cell_x, mouse_cell_y = mouse_cell
                    ACTIONS.append({
                        "type" : "VACCINATE",
                        "cell_x" : mouse_cell_x,
                        "cell_y" : mouse_cell_y
                    })

        return ACTIONS

    def pre_render(self):
        _actions = self.command_handler()
        self.screen.fill(self.COLORS.WHITE)
        self.draw_grid()
        self.draw_stats()
        self.draw_mouse_hightlight()
        return _actions

    def post_render(self):
        pygame.display.update()


if __name__ == "__main__":

    grid_size=(50,50)
    renderer = Renderer(grid_size=grid_size)
    renderer.setup()
    x = 0
    y = 0

    while True:
        renderer.pre_render()
        renderer.draw_cell(x, y)
        renderer.post_render()

        x+=1
        y+=1
        x%=grid_size[0]
        y%=grid_size[1]

        # time.sleep(0.1)
