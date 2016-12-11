from mesa import Agent
import random


class Tourist(Agent):
    """Represents a single Tourist cell in the simulation."""

    def __init__(self, unique_id, model, position, energy=1, moore=True, add_to_schedule=True,
                 probability=0.0, position_in_trail=0, direction='forward',
                 prob_forward=0.9, prob_backward=0.09, prob_stay=0.01):

        """
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        """
        super().__init__(unique_id, model)
        self.moore = moore
        self.model = model
        self._direction = direction
        self._model = model
        self._energy = energy
        self._pos = position
        self._position_in_trail = position_in_trail
        self._probability = probability
        self._prob_forward = prob_forward
        self._prob_backward = prob_backward
        self._prob_stay = prob_stay

        if add_to_schedule:
            self.model.schedule_tourists.add(self)

        self.model.grid.place_agent(self, position)

    def tourist_multiplication(self):
        if self._position_in_trail < self.model.trail.get_length()-1:
            geo_position = self.model.trail.trail[self._position_in_trail + 1].get_geo_pos()

            tourist_forward = Tourist(position=geo_position, unique_id=1, model=self.model,
                                      add_to_schedule=False, position_in_trail=self._position_in_trail + 1,
                                      probability=self.get_prob_forward())

            self.model.trail.trail[self._position_in_trail].add_tourist(tourist_forward)

            self.model.grid.place_agent(tourist_forward, geo_position)

        if self._position_in_trail > 1:
            geo_position = self.model.trail.trail[self._position_in_trail - 1].get_geo_pos()

            tourist_back = Tourist(position=geo_position, unique_id=1, model=self.model,
                                   add_to_schedule=False, position_in_trail=self._position_in_trail - 1,
                                   probability=self.get_prob_backward())

            self.model.grid.place_agent(tourist_back, geo_position)

    def advance(self):
        """
        Step one cell in any allowable direction with concrete probability distribution.
        0.89 - forward, 0.1 - return, 0.01 - stay in place
        """
        self.tourist_multiplication()

    def get_energy(self):
        return self._energy

    def set_energy(self, energy):
        self._energy += energy

    def get_position_in_trail(self):
        return self._position_in_trail

    def set_position_in_trail(self, pos):
        self._position_in_trail = pos

    def get_position(self):
        return self._pos

    def set_position(self, pos):
        self._pos = pos

    def get_direction(self):
        return self._direction

    def set_direction(self, direction):
        self._direction = direction

    def get_probability(self):
        return self._probability

    def set_probability(self, probability):
        self._probability = probability

    def get_prob_forward(self):
        return self._prob_forward

    def get_prob_stay(self):
        return self._prob_stay

    def get_prob_backward(self):
        return self._prob_backward


class TrailElement(Agent):
    def __init__(self, unique_id, model):
        """
        Create a cell of trail, at the given x, y position.
        """
        super().__init__(unique_id, model)
        self._tourists = []

    def advance(self):
        resultant_probability = 1
        i = 0
        resultant_tourist = None
        for tourist in self._tourists:
            resultant_probability *= tourist.get_probability()
            x, y = tourist.get_position()
            pos_in_trail = tourist.get_position_in_trail()
            self.model.grid[x][y].remove(tourist)
            i += 1
            if i == len(self._tourists):
                resultant_tourist = Tourist(position=(x, y), unique_id=1, model=self.model,
                                            add_to_schedule=True, position_in_trail=pos_in_trail,
                                            probability=resultant_probability)
        self._tourists = []
        if resultant_tourist is not None:
            self._tourists.append(resultant_tourist)

    def get_tourists(self):
        return self._tourists

    def set_tourists(self, tourists):
        self._tourists = tourists

    def get_geo_pos(self):
        return self.unique_id

    def add_tourist(self, tourist):
        self._tourists.append(tourist)


class Trail:
    def __init__(self, model, trail_iter=200, tourists=1):

        self.model = model
        self.trail = []
        self._trail_iter = trail_iter
        self._trail_length = 0
        self._start_position = None
        self._tourists = tourists

        trail = []
        length = 0
        x = random.randrange(round(self.model.width))
        y = random.randrange(round(self.model.height))
        self.set_trail_start((x, y))

        trail_element = TrailElement((x, y), self.model)
        trail.append(trail_element)
        self.model.schedule_trail_elements.add(trail_element)
        self.model.grid.place_agent(trail_element, (x, y))

        length += 1

        for i in range(1, self.get_iter()):
            next_trail = self.model.grid.get_neighborhood((x, y), moore=True)
            (temp_x, temp_y) = random.choice(next_trail)
            next_next_trail = self.model.grid.get_neighborhood((temp_x, temp_y), moore=True)

            trails_number = 0
            for cell in next_next_trail:

                content = self.model.grid.get_cell_list_contents([cell])
                if content:
                    trails_number += 1

            if trails_number < 2:
                trail_element = TrailElement((temp_x, temp_y), self.model)
                trail.append(trail_element)
                self.model.schedule_trail_elements.add(trail_element)
                self.model.grid.place_agent(trail_element, (temp_x, temp_y))
                length += 1
                x = temp_x
                y = temp_y

        self.model.grid.place_agent(Tourist(position=self.get_trail_start(), unique_id=1, model=self.model),
                                    self.get_trail_start())

        self.trail = trail
        self.set_length(length)

        self.advance_counter = self.get_tourists()

    def agents_count(self):
        trail = self.trail
        tourists_number = 0
        for cell in trail:
            tourists_number += cell.get_tourists_number()
        return tourists_number

    def get_length(self):
        return self._trail_length

    def get_iter(self):
        return self._trail_iter

    def get_trail_start(self):
        return self._start_position

    def get_tourists(self):
        return self._tourists

    def set_tourists(self, tourists):
        self._tourists = tourists

    def set_length(self, length):
        self._trail_length = length

    def set_trail_start(self, start):
        self._start_position = start
