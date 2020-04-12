#!/usr/bin/env python

import numpy as np

import pyglet

from pyglet.gl import glClearColor

from rogi_rl.colors import Colors, ColorMap
from rogi_rl.agent_state import AgentState

from gym.envs.classic_control import rendering


class Renderer:
    def __init__(self, grid_size=(30, 30)):
        self.grid_size = grid_size

        self.COLORS = Colors()
        self.COLOR_MAP = ColorMap()
        self.setup_constants()
        self.setup_stats()

        self.screen = None

    def setup_constants(self):

        self.AGENT_STATUS_FONT_SIZE = 10
        self.AGENT_STATUS_LINE_SPACE = 10

        self.CONTROL_PANEL_WIDTH = 200
        self.TOP_PANEL_HEIGHT = 20
        self.MARGIN = 5

        # CELL_PROPERTIES
        self.CELL_WIDTH = int(800 / self.get_grid_width())
        self.CELL_HEIGHT = int(800 / self.get_grid_height())
        self.CELL_PADDING = int(self.CELL_WIDTH / 5)

        self.STATE_CELL_WIDTH = self.CELL_WIDTH - 2 * self.CELL_PADDING
        self.STATE_CELL_HEIGHT = self.CELL_HEIGHT - 2 * self.CELL_PADDING

        self.MOUSE_HIGHLIGHTER_WIDTH = 3

        # GRID_PROPERTIES
        self.GRID_BASE_X = self.MARGIN + self.CONTROL_PANEL_WIDTH \
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
            self.stats[f"population.{_state.name}"] = 0

        # Simulation Progress
        self.stats["SIMULATION_TICKS"] = 0
        # Game Progress
        self.stats["GAME_TICKS"] = 0
        self.stats["VACCINE_BUDGET"] = 0

        self.stats['PREV_ACTIONS'] = []

        self.stats["SCORE"] = 0

        self.stats["TEXT_STRINGS"] = {}

        self.WIDTH = self.GRID_MAX_X + self.MARGIN
        self.HEIGHT = self.GRID_MAX_Y + self.MARGIN

    def get_cell_base(self, cell_x, cell_y):
        return (
            self.GRID_BASE_X + cell_x * self.CELL_WIDTH,
            self.GRID_BASE_Y + cell_y * self.CELL_HEIGHT,
        )

    def get_grid_width(self):
        return self.grid_size[0]

    def get_grid_height(self):
        return self.grid_size[1]

    def setup(self):
        if self.screen is None:
            self.screen = rendering.Viewer(self.WIDTH,
                                           self.HEIGHT)
            glClearColor(*self.convert_gym_color(self.COLORS.WHITE), 1)

    def draw_stats(self):
        top_x = self.MARGIN
        top_y = self.GRID_MAX_Y - \
            (self.GRID_BASE_Y + self.MARGIN + self.AGENT_STATUS_FONT_SIZE
                + 2 + self.AGENT_STATUS_LINE_SPACE)
        ################################################################
        ################################################################
        dict_texts = {}

        # Simulation Statistics Header
        _text_string = "Simulation Statistics"

        _state_text_color = self.COLOR_MAP.get_color("AGENT_STATE_TEXT_COLOR")

        dict_texts[_text_string] = pyglet.text.Label(
                                    _text_string,
                                    font_size=int(
                                                self.AGENT_STATUS_FONT_SIZE
                                                + 2),
                                    x=top_x, y=top_y,
                                    color=(*_state_text_color, 255))

        top_y -= self.AGENT_STATUS_LINE_SPACE + self.AGENT_STATUS_FONT_SIZE
        ################################################################
        ################################################################
        # Line
        ################################################################
        rect_base_x = top_x
        rect_base_y = top_y

        rect_width = self.CONTROL_PANEL_WIDTH
        rect_height = 2

        self.draw_standard_rect(_state_text_color, (
            rect_base_x, rect_base_x + rect_width,
            rect_base_y + rect_height, rect_base_y
        ))

        top_y -= 2 * rect_height + self.AGENT_STATUS_LINE_SPACE
        ################################################################
        ################################################################
        # Render AgentState Values
        ################################################################

        for _state in AgentState:
            _text_string = str(self.stats[f"population.{_state.name}"])
            _text_string += " "
            _text_string += _state.name

            _font_size = int(self.AGENT_STATUS_FONT_SIZE)
            dict_texts[_text_string] = \
                pyglet.text.Label(_text_string, font_size=_font_size,
                                  x=top_x, y=top_y,
                                  color=(
                                      *self.COLOR_MAP.get_color(_state), 255))

            top_y -= self.AGENT_STATUS_LINE_SPACE + self.AGENT_STATUS_FONT_SIZE
        ################################################################
        ################################################################
        # Line
        ################################################################
        rect_base_x = top_x
        rect_base_y = top_y

        rect_width = self.CONTROL_PANEL_WIDTH
        rect_height = 2

        self.draw_standard_rect(
            self.COLOR_MAP.get_color("AGENT_STATE_TEXT_COLOR"), (
                rect_base_x, rect_base_x + rect_width,
                rect_base_y + rect_height, rect_base_y))

        top_y -= 2 * rect_height + self.AGENT_STATUS_LINE_SPACE
        ################################################################
        ################################################################
        # Simulation Progress Header
        _text_string = "Progress"
        _font_size = int(self.AGENT_STATUS_FONT_SIZE + 2)
        _color = (*_state_text_color, 255)
        dict_texts[_text_string] = pyglet.text.Label(_text_string,
                                                     font_size=_font_size,
                                                     x=top_x, y=top_y,
                                                     color=_color)

        top_y -= self.AGENT_STATUS_LINE_SPACE + self.AGENT_STATUS_FONT_SIZE
        ################################################################
        ################################################################
        # Line
        ################################################################
        rect_base_x = top_x
        rect_base_y = top_y

        rect_width = self.CONTROL_PANEL_WIDTH
        rect_height = 2

        _state_text_color = self.COLOR_MAP.get_color("AGENT_STATE_TEXT_COLOR")
        self.draw_standard_rect(_state_text_color, (
            rect_base_x, rect_base_x + rect_width,
            rect_base_y + rect_height, rect_base_y
        ))

        top_y -= 2 * rect_height + self.AGENT_STATUS_LINE_SPACE

        for _state in ["SIMULATION_TICKS", "GAME_TICKS", "VACCINE_BUDGET"]:
            _text_string = str(self.stats[_state])
            _text_string += " "
            _text_string += _state

            _font_size = int(self.AGENT_STATUS_FONT_SIZE)
            _color = (*_state_text_color, 255)

            dict_texts[_text_string] = pyglet.text.Label(_text_string,
                                                         font_size=_font_size,
                                                         x=top_x, y=top_y,
                                                         color=_color)

            top_y -= self.AGENT_STATUS_LINE_SPACE + self.AGENT_STATUS_FONT_SIZE

        ################################################################
        ################################################################
        # Line
        ################################################################
        rect_base_x = top_x
        rect_base_y = top_y

        rect_width = self.CONTROL_PANEL_WIDTH
        rect_height = 2

        _state_text_color = self.COLOR_MAP.get_color("AGENT_STATE_TEXT_COLOR")
        self.draw_standard_rect(_state_text_color, (
            rect_base_x, rect_base_x + rect_width,
            rect_base_y + rect_height, rect_base_y
        ))

        top_y -= 2 * rect_height + self.AGENT_STATUS_LINE_SPACE

        _text_string = "Recent Actions"
        _font_size = int(self.AGENT_STATUS_FONT_SIZE + 2)

        dict_texts[_text_string] = pyglet.text.Label(_text_string,
                                                     font_size=_font_size,
                                                     x=top_x, y=top_y,
                                                     color=_color)

        top_y -= self.AGENT_STATUS_LINE_SPACE + self.AGENT_STATUS_FONT_SIZE

        ################################################################
        ################################################################
        # Line
        ################################################################
        rect_base_x = top_x
        rect_base_y = top_y

        rect_width = self.CONTROL_PANEL_WIDTH
        rect_height = 2

        _state_text_color = self.COLOR_MAP.get_color("AGENT_STATE_TEXT_COLOR")
        self.draw_standard_rect(_state_text_color, (
            rect_base_x, rect_base_x + rect_width,
            rect_base_y + rect_height, rect_base_y
        ))

        top_y -= 2 * rect_height + self.AGENT_STATUS_LINE_SPACE

        prev_actions = list(self.stats['PREV_ACTIONS'])
        _font_size = int(self.AGENT_STATUS_FONT_SIZE)

        for _action in prev_actions[::-1]:
            _text_string = str(_action)
            dict_texts[_text_string] = pyglet.text.Label(_text_string,
                                                         font_size=_font_size,
                                                         x=top_x, y=top_y,
                                                         color=_color)

            top_y -= self.AGENT_STATUS_LINE_SPACE + self.AGENT_STATUS_FONT_SIZE

        _text_string = "Step Reward"
        _text_string += ":"
        _text_string += str(self.stats['SCORE'])
        _font_size = int(self.AGENT_STATUS_FONT_SIZE+2)
        _x = self.MARGIN
        _y = self.HEIGHT - self.MARGIN - self.AGENT_STATUS_FONT_SIZE
        dict_texts[_text_string] = pyglet.text.Label(
                                    _text_string, font_size=_font_size,
                                    x=_x,
                                    y=_y,
                                    color=(*self.COLORS.RED, 255))

        self.stats["TEXT_STRINGS"] = dict_texts

    def update_stats(self, key, value):
        if type(value) != str:
            raise Exception("renderer.stats value is not String")
        self.stats[key] = value
        # print(self.stats)

    def draw_grid(self, color):
        # Draw Vertical Ticks
        for _x_coord in range(self.get_grid_width() + 1):
            cell_base = self.get_cell_base(_x_coord, 0)
            start_coord = (
                cell_base[0],
                self.GRID_BASE_Y
            )
            end_coord = (
                cell_base[0],
                self.GRID_MAX_Y
            )
            self.draw_standard_line(
                color,
                start_coord, end_coord)

        # Draw Horizontal Ticks
        for _y_coord in range(self.get_grid_height() + 1):
            cell_base = self.get_cell_base(0, _y_coord)
            start_coord = (
                self.GRID_BASE_X,
                cell_base[1]
            )
            end_coord = (
                self.GRID_MAX_X,
                cell_base[1]
            )
            self.draw_standard_line(
                color,
                start_coord, end_coord)

    def draw_cell(self, cell_x, cell_y, color=False):
        cell_base = self.get_cell_base(cell_x, cell_y)

        if not color:
            color = self.COLORS.BLUE

        rect_base_x = cell_base[0] + self.CELL_PADDING
        rect_base_y = cell_base[1] + self.CELL_PADDING

        rect_width = self.STATE_CELL_WIDTH
        rect_height = self.STATE_CELL_HEIGHT

        self.draw_standard_rect(color, (
            rect_base_x, rect_base_x + rect_width,
            rect_base_y + rect_height, rect_base_y
        ))

    def draw_standard_line(self, color, start_coord, end_coord):
        line = rendering.Line(start_coord, end_coord)
        line.set_color(*self.convert_gym_color(color))
        self.screen.add_geom(line)

    def draw_standard_rect(self, color, rect_dims):
        rect_base_x, rect_base_y, rect_width, rect_height = rect_dims
        rectangle = rendering.FilledPolygon(
            [
                (rect_base_x, rect_height),
                (rect_base_x, rect_width),
                (rect_base_y, rect_width),
                (rect_base_y, rect_height)
            ])
        rectangle.set_color(*self.convert_gym_color(color))
        self.screen.add_geom(rectangle)

    def convert_gym_color(self, color: Colors):
        return np.array(color) / 255

    def pre_render(self):
        self.draw_grid(self.COLORS.GREY)
        self.draw_stats()
        return False

    def prepare_render(self):
        self.screen.window.clear()
        self.screen.window.switch_to()
        self.screen.window.dispatch_events()
        return False

    def post_render(self, return_rgb_array=False):
        """
        Some part of the code is taken from the file
        https://github.com/openai/gym/blob/master/gym/envs/classic_control/rendering.py
        The render method of class `viewer` clears the window.
        This also results in any text on the screen to be lost
        Hence we copy the contents of the `render` function and modify it
        """

        self.prepare_render()

        dict_texts = self.stats['TEXT_STRINGS']

        for key in dict_texts.keys():
            cur_text_label = dict_texts[key]
            cur_text_label.draw()

        self.screen.transform.enable()
        for geom in self.screen.geoms:
            geom.render()
        for geom in self.screen.onetime_geoms:
            geom.render()
        self.screen.transform.disable()
        self.screen.window.flip()
        self.screen.onetime_geoms = []

        arr = None
        if return_rgb_array:
            buffer = pyglet.image.get_buffer_manager().get_color_buffer()
            image_data = buffer.get_image_data()
            arr = np.frombuffer(image_data.get_data(), dtype=np.uint8)
            # In https://github.com/openai/gym-http-api/issues/2, we
            # discovered that someone using Xmonad on Arch was having
            # a window of size 598 x 398, though a 600 x 400 window
            # was requested. (Guess Xmonad was preserving a pixel for
            # the boundary.) So we use the buffer height/width rather
            # than the requested one.
            arr = arr.reshape(buffer.height, buffer.width, 4)
            arr = arr[::-1, :, 0:3]
        self.screen.window.flip()
        self.onetime_geoms = []
        return arr if return_rgb_array else self.screen.isopen


if __name__ == "__main__":

    grid_size = (50, 50)
    renderer = Renderer(grid_size=grid_size)
    renderer.setup()
    x = 0
    y = 0

    while True:
        renderer.pre_render()
        renderer.draw_cell(x, y)

        renderer.post_render()

        x += 1
        y += 1
        x %= grid_size[0]
        y %= grid_size[1]
