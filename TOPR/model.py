from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

from TOPR.agents import Trail, TrailElement
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
        self.schedule_tourists = SimultaneousActivation(self)
        self.schedule_trail_elements = SimultaneousActivation(self)
        self.step_performed = 1
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.trail = Trail(self)
        self.maximum_probability = 0
        self.minimum_probability = 1

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.maximum_probability = 0
        self.minimum_probability = 1
        self.schedule_tourists.step()
        self.schedule_tourists = SimultaneousActivation(self)
        for element in self.trail.trail:
            if type(element) is TrailElement:
                if element.get_trail_gradient() == self.step_performed:
                    self.schedule_trail_elements.add(element)
        self.schedule_trail_elements.step()
        self.step_performed += 1
