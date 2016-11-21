from mesa import Agent


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
        self.__energy = energy
        self.__pos = pos
        self.moore = moore

    def advance(self):
        """
        Step one cell in any allowable direction with concrete probability distribution.
        0.89 - forward, 0.1 - return, 0.01 - stay in place
        """

        next_moves = self.model.grid.get_neighborhood(self.get_position(), self.moore)
        trail_indicator_prev = 0
        trail_indicator = 0

        # set probability that tourist stay in the same place
        x, y = self.get_position()
        elements = list(self.model.grid[x][y])
        for i in range(0, len(elements)):
            if type(elements[i]) is TrailElement:
                trail = elements[i]
                trail.set_probability(0.01)

        for cell in next_moves:
            x, y = cell
            temp = list(self.model.grid[x][y])
            if temp:
                for i in range(0, len(temp)):
                    if type(temp[i]) is TrailElement:
                        trail_indicator = trail.get_position_in_trail()

            if trail_indicator > trail_indicator_prev:
                self.model.grid.move_agent(self, cell)
                # set probability that tourist move forward
                trail.set_probability(0.89)
                trail_indicator_prev = trail_indicator

            if trail_indicator < trail_indicator_prev:
                # set probability that tourist move backward
                trail.set_probability(0.1)

    def get_energy(self):
        return self.__energy

    def set_energy(self, energy):
        self.__energy += energy

    def get_position(self):
        return self.__pos

    def set_position(self, pos):
        self.__pos = pos


class TrailElement(Agent):
    def __init__(self, pos, model, trailposition):
        """
        Create a cell, in the given state, at the given x, y position.
        """
        super().__init__(pos, model)
        # self.id = id
        self.__probability = 0
        self.__trailposition = trailposition

    @staticmethod
    def advance():
        return

    def get_probability(self):
        return self.__probability

    def set_probability(self, probability):
        self.__probability += probability

    def get_position_in_trail(self):
        return self.__trailposition

    def set_position_in_trail(self, position_in_trail):
        self.__trailposition += position_in_trail
