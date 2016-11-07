from mesa import Agent
import random

# import random


class Tourist(Agent):
    """Represents a single Tourist cell in the simulation."""

    def __init__(self, pos, model, speed=5, moore=True, trail_indicator=0):
        """
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        """
        super().__init__(pos, model)
        self.speed = speed
        self.moore = moore
        self.trail_indicator = trail_indicator
        self.trail_indicator_prev = trail_indicator
    # @property
    # def neighbors(self):
    #     return self.model.grid.neighbor_iter((self.x, self.y), True)

    def advance(self):
        """
        Step one cell in any allowable direction.
        """

        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore)
        for cell in next_moves:
            # temp = self.model.grid.get_cell_list_contents([cell])
            x, y = cell

            temp = self.model.grid[x][y]
            if temp:
                self.trail_indicator = list(temp)[0].id

            if self.trail_indicator > self.trail_indicator_prev:
                self.model.grid.move_agent(self, cell)
                self.trail_indicator_prev = self.trail_indicator

class Trail(Agent):
    def __init__(self, pos, model, unique_id):
        """
        Create a cell, in the given state, at the given x, y position.
        """
        super().__init__(pos, model)
        self.id = unique_id

    @staticmethod
    def advance():
        return
