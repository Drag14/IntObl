from mesa import Agent
import random
from TOPR.config import height, width, initial_tourist


class Tourist(Agent):
    """Represents a single Tourist cell in the simulation."""

    def __init__(self, pos, model, energy=5, moore=True):
        """
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        """
        super().__init__(pos, model)
        self.moore = moore
        self.__direction = 'forward'
        self.__model = model
        self.__energy = energy
        self.__pos = pos

        self.model.grid.place_agent(self, pos)
        self.model.schedule.add(self)

        for i in range(0, initial_tourist - 1):
            x = random.randrange(width)
            y = random.randrange(height)
            self.model.grid.place_agent(self, (x, y))
            self.model.schedule.add(self)

    def advance(self):
        """
        Step one cell in any allowable direction with concrete probability distribution.
        0.89 - forward, 0.1 - return, 0.01 - stay in place
        """
        model = self.get_model()
        x, y = self.get_position()

        elements = list(model.grid[x][y])

        for i in range(0, len(elements)):
            if type(elements[i]) is TrailElement:
                trail_position = elements[i].get_position_in_trail()  # get trail_element position in trail

        # model.trail.

    def get_energy(self):
        return self.__energy

    def set_energy(self, energy):
        self.__energy += energy

    def get_position(self):
        return self.__pos

    def set_position(self, pos):
        self.__pos = pos

    def get_direction(self):
        return self.__direction

    def set_direction(self, direction):
        self.__direction = direction

    def set_model(self, model):
        self.__model = model

    def get_model(self):
        return self.__model


class TrailElement(Agent):
    def __init__(self, pos, model, trailposition):
        """
        Create a cell of trail, at the given x, y position.
        """
        super().__init__(pos, model)
        # self.id = id
        self.__pos = pos
        self.__probability = 0
        self.__trailposition = trailposition

    @staticmethod
    def advance():
        return

    def get_probability(self):
        return self.__probability

    def get_geo_pos(self):
        return self.__pos

    def get_position_in_trail(self):
        return self.__trailposition

    def set_probability(self, probability):
        self.__probability *= probability

    def set_geo_pos(self, pos):
        self.__pos = pos

    def set_position_in_trail(self, position_in_trail):
        self.__trailposition = position_in_trail


class Trail:
    def __init__(self, model, trail_iter=200):
        self.__model = model
        self.__trail = []
        self.__trail_iter = trail_iter
        self.__trail_length = 0
        self.__start_position = None

    def create_trail(self):
        model = self.get_model()
        x = random.randrange(round(model.width))
        y = random.randrange(round(model.height))
        self.set_trail_start((x, y))

        trail_element = TrailElement((x, y), self, 0)
        self.append_to_trail(trail_element)
        model.grid.place_agent(trail_element, (x, y))

        for i in range(1, self.get_iter()):
            next_trail = model.grid.get_neighborhood((x, y), moore=True)
            (temp_x, temp_y) = random.choice(next_trail)
            next_next_trail = model.grid.get_neighborhood((temp_x, temp_y), moore=True)

            trails_number = 0
            for cell in next_next_trail:
                if model.grid.get_cell_list_contents([cell]):
                    trails_number += 1

            if trails_number < 2:
                trail_element = TrailElement((x, y), self, i)
                self.append_to_trail(trail_element)
                model.grid.place_agent(trail_element, (temp_x, temp_y))
                x = temp_x
                y = temp_y

    def evaluate(self):
        trail_elements = self.get_trail()
        for elements in trail_elements:
            elements.evaluate()

    def get_model(self):
        return self.__model

    def get_length(self):
        return self.__trail_length

    def get_iter(self):
        return self.__trail_iter

    def get_trail(self):
        return self.__trail

    def get_trail_start(self):
        return self.__start_position

    def set_trail(self, elements):
        self.__trail = elements

    def set_length(self, length):
        self.__trail_length = length

    def set_model(self, model):
        self.__model = model

    def set_trail_start(self, start):
        self.__start_position = start

    def append_to_trail(self, element):
        self.__trail.append(element)
        self.__trail_length += 1
