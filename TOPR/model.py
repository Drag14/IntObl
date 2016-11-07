import random

from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

from TOPR.agents import Tourist, Trail
from TOPR.config import height, width


class TOPRAction(Model):
    """
    Represents the 2-dimensional array of cells in Conway's
    Game of Life.
    """

    def __init__(self, h=height, w=width, initial_tourist=4):
        """
        Create a action area of (height, width) cells.
        """
        super().__init__()
        self.height = h
        self.width = w
        self.initial_tourist = initial_tourist
        self.initial_trails = initial_tourist
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.schedule = SimultaneousActivation(self)

        # Create tourists:
        for i in range(self.initial_tourist):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            tourist = Tourist((x, y), self)
            self.grid.place_agent(tourist, (x, y))
            self.schedule.add(tourist)

        # Create trail
        for i in range(50):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            trail = Trail((x, y), self)
            self.grid.place_agent(trail, (x, y))
            self.schedule.add(trail)

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.schedule.step()
