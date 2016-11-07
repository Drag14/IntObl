import random

from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

from TOPR.agents import Tourist, Trail
from TOPR.config import height, width, trail_length, initial_tourist


class TOPRAction(Model):
    """
    Represents the 2-dimensional array of cells in Conway's
    Game of Life.
    """

    def __init__(self, h=height, w=width, tourists=initial_tourist):
        """
        Create a action area of (height, width) cells.
        """
        super().__init__()
        self.height = h
        self.width = w
        self.tourists = tourists
        self.initial_trails = initial_tourist
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.trail_start_position = (0, 0)

        self.create_trail()

        # # Create tourists:
        # for i in range(self.tourists):
        #     x = random.randrange(self.width)
        #     y = random.randrange(self.height)
        #     tourist = Tourist((x, y), self)
        #     self.grid.place_agent(tourist, (x, y))
        #     self.schedule.add(tourist)

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.schedule.step()

    def create_trail(self):
        x = random.randrange(round(self.width/5))
        y = random.randrange(round(self.height/5))
        self.trail_start_position = (x, y)
        self.grid.place_agent(Trail((x, y), self), (x, y))
        self.schedule.add(Trail((x, y), self))

        # Create trail
        for i in range(trail_length):
            next_trail = self.grid.get_neighborhood((x, y), moore=True)
            while True:
                (x, y) = random.choice(next_trail)
                temp_x = x
                temp_y = y
                temp_next_trail = self.grid.get_neighborhood((temp_x, temp_y), moore=True)
                trails_number = 0
                for cells in temp_next_trail:
                    print(isinstance(self.grid.get_cell_list_contents([cells]), Trail))
                    if self.grid.get_cell_list_contents([cells]) is Trail:  # error - returns list / not trail etc.
                        # print("it's trail")
                        trails_number += 1

                if trails_number < 2:
                    self.grid.place_agent(Trail(next_trail, self), (x, y))
                    self.schedule.add(Trail((x, y), self))
                    break

