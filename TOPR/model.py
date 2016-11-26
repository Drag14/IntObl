from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

from TOPR.agents import Trail
from TOPR.config import height, width


class TOPRAction(Model):
    """
    Represents the 2-dimensional array of cells
    """

    def __init__(self, h=height, w=width):
        """
        Create a action area of (height, width) cells.
        """
        super().__init__()
        self.height = h
        self.width = w
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.trail = Trail(self, tourists=1)

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.schedule.step()
