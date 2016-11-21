import random

from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

from TOPR.agents import Tourist, TrailElement, Trail
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
        self.trail = Trail(self)
        self.trail.create_trail()

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.schedule.step()

    # Create tourist
    def create_tourist(self):
        start = self.trail.get_trail_start()
        print(start)
        tourist = Tourist(start, self)
        self.grid.place_agent(tourist, start)
        self.schedule.add(tourist)

        for i in range(0, self.tourists - 1):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            tourist = Tourist((x, y), self)
            self.grid.place_agent(tourist, (x, y))
            self.schedule.add(tourist)

