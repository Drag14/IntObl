from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

from TOPR.agents import Trail, Tourist
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
        self.tourists_on_trail = 0
        self.frequency = 5
        self.steps_of_tourist_1 = 1
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.schedule_tourists = SimultaneousActivation(self)
        self.schedule_trail_elements = SimultaneousActivation(self)
        self.trail = Trail(self, trail_iter=100, tourists=1)

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.schedule_tourists.step()
        self.schedule_tourists = SimultaneousActivation(self)
        self.schedule_trail_elements.step()
