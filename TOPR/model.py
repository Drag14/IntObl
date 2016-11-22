from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

from TOPR.agents import Tourist, Trail
from TOPR.config import height, width, initial_tourist


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
        self.tourist = Tourist(self.trail.get_trail_start(), self)

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.schedule.step()
