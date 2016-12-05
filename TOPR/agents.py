from mesa import Agent
import random


class Tourist(Agent):
    """Represents a single Tourist cell in the simulation."""

    def __init__(self, pos, model, energy=1, moore=True, add_to_schedule=True,
                 probability=1, position_iter=0, direction='forward', tourist_id=1,
                 prob_forward=0.9, prob_backward=0.09, prob_stay=0.01):

        """
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        """
        super().__init__(pos, model)
        self.moore = moore
        self.model = model
        self.__direction = direction
        self.__model = model
        self.__energy = energy
        self.__pos = pos
        self.__position_iter = position_iter
        self.__probability = probability
        self.__tourist_id = tourist_id
        self.__prob_forward = prob_forward
        self.__prob_backward = prob_backward
        self.__prob_stay = prob_stay

        if add_to_schedule:
            self.model.schedule.add(self)

        self.model.grid.place_agent(self, pos)

    def multiply_tourists(self):
        tourists_to_add = []

        if self.get_direction() == 'forward':

            self.set_direction('stay')

            if self.get_position_iter() < self.model.trail.get_length():
                self.set_probability(self.get_prob_forward())
                geo_position = self.model.trail.get_trail()[self.get_position_iter() + 1].get_geo_pos()

                tourist_forward = Tourist(geo_position, self.model, direction='forward',
                                          add_to_schedule=False, position_iter=self.get_position_iter())
                self.model.grid.place_agent(tourist_forward, geo_position)
                tourists_to_add.append(tourist_forward)

            if self.get_position_iter() > 1:
                self.set_probability(self.get_prob_backward())
                geo_position = self.model.trail.get_trail()[self.get_position_iter() - 1].get_geo_pos()
                tourist_back = Tourist(geo_position, self.model, direction='backward',
                                       add_to_schedule=False, position_iter=self.get_position_iter())
                self.model.grid.place_agent(tourist_back, geo_position)
                tourists_to_add.append(tourist_back)

        elif self.get_direction() == 'backward':
            self.set_direction('stay')

            if self.get_position_iter() < self.model.trail.get_length():
                self.set_probability(self.get_prob_backward())
                geo_position = self.model.trail.get_trail()[self.get_position_iter() + 1].get_geo_pos()

                tourist_forward = Tourist(geo_position, self.model, direction='forward',
                                          add_to_schedule=False, position_iter=self.get_position_iter())
                self.model.grid.place_agent(tourist_forward, geo_position)
                tourists_to_add.append(tourist_forward)

            if self.get_position_iter() > 1:
                self.set_probability(self.get_prob_forward())
                geo_position = self.model.trail.get_trail()[self.get_position_iter() - 1].get_geo_pos()
                tourist_back = Tourist(geo_position, self.model, direction='backward',
                                       add_to_schedule=False, position_iter=self.get_position_iter())
                self.model.grid.place_agent(tourist_back, geo_position)
                tourists_to_add.append(tourist_back)

        self.model.trail.set_tourists(self.model.trail.get_tourists()+len(tourists_to_add))
        return tourists_to_add

    def move(self):
        if self.get_direction() == 'forward' and self.get_position_iter() < self.model.trail.get_length()-1:
            self.model.grid.move_agent(self, self.model.trail.
                                       get_trail()[self.get_position_iter() + 1].get_geo_pos())
            self.set_probability(self.get_prob_forward())
            self.increment_position_iter()

        elif self.get_direction() == 'backward' and 1 < self.get_position_iter():
            self.model.grid.move_agent(self, self.model.trail.
                                       get_trail()[self.get_position_iter() - 1].get_geo_pos())
            self.set_probability(self.get_prob_forward())
            self.decrement_position_iter()

        elif self.get_direction() == 'stay':
            self.set_probability(self.get_prob_stay())

    def advance(self):
        """
        Step one cell in any allowable direction with concrete probability distribution.
        0.89 - forward, 0.1 - return, 0.01 - stay in place
        """
        tourists = []

        if self.model.trail.advance_counter > 0:
            if self.model.trail.get_length() >= self.model.steps_performed > 0 == self. \
                    model.steps_performed % self.model.frequency:
                tourists = self.multiply_tourists()
            else:
                self.move()

            if self.model.trail.get_remembered_tourists():
                for tourist in self.model.trail.get_remembered_tourists():
                    self.model.schedule.add(tourist)
                self.model.trail.clear_remember_tourists()

            self.model.trail.remember_tourists(tourists)
            self.model.trail.advance_counter -= 1

    def decrement_position_iter(self):
        self.__position_iter -= 1

    def increment_position_iter(self):
        self.__position_iter += 1

    def get_energy(self):
        return self.__energy

    def set_energy(self, energy):
        self.__energy += energy

    def get_position_iter(self):
        return self.__position_iter

    def set_position_iter(self, pos):
        self.__position_iter = pos

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

    def get_probability(self):
        return self.__probability

    def set_probability(self, probability):
        self.__probability = probability

    def get_tourist_number(self):
        return self.__tourist_id

    def set_tourist_number(self, num_id):
        self.__tourist_id = num_id

    def get_prob_forward(self):
        return self.__prob_forward

    def get_prob_stay(self):
        return self.__prob_stay

    def get_prob_backward(self):
        return self.__prob_backward


class TrailElement:
    def __init__(self, pos, trailposition):
        """
        Create a cell of trail, at the given x, y position.
        """

        self.__pos = pos
        self.__trailposition = trailposition
        self.__tourists = []

    def add_tourist(self, tourist):
        tourists = self.get_tourists()
        tourists.append(tourist)
        self.set_tourists(tourists)

    def get_geo_pos(self):
        return self.__pos

    def get_position_in_trail(self):
        return self.__trailposition

    def get_tourists(self):
        return self.__tourists

    def set_geo_pos(self, pos):
        self.__pos = pos

    def set_position_in_trail(self, position_in_trail):
        self.__trailposition = position_in_trail

    def set_tourists(self, tourists):
        self.__tourists = tourists

    def get_tourists_number(self):
        return len(self.get_tourists())


class Trail(Agent):
    def __init__(self, model, trail_iter=200, tourists=1):
        super().__init__(1, model)
        self.__trail = []
        self.__trail_iter = trail_iter
        self.__trail_length = 0
        self.__start_position = None
        self.__tourists = tourists
        self.__last_tourists = []
        self.advance_counter = 0

        trail = []
        length = 0
        x = random.randrange(round(self.model.width))
        y = random.randrange(round(self.model.height))
        self.set_trail_start((x, y))

        trail_element = TrailElement((x, y), 0)
        trail.append(trail_element)

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
                trail_element = TrailElement((temp_x, temp_y), i)
                trail.append(trail_element)
                self.model.grid.place_agent(trail_element, (temp_x, temp_y))
                length += 1
                x = temp_x
                y = temp_y

        self.set_trail(trail)
        self.set_length(length)

        for i in range(0, self.get_tourists()):
            self.get_trail()[0].add_tourist(Tourist(self.get_trail_start(), self.model))

        self.advance_counter = self.get_tourists()
        self.model.schedule.add(self)

    def advance(self):
        self.advance_counter = self.get_tourists()
        return

    def get_trail_from_position(self, position):
        trail = self.get_trail()
        length = self.get_length()
        if position < 1 or position >= length:
            return
        else:
            return trail[position]

    def remember_tourists(self, tourists):
        self.__last_tourists = tourists

    def clear_remember_tourists(self):
        del self.__last_tourists[:]

    def get_remembered_tourists(self):
        return self.__last_tourists

    def get_next_trail(self, position):
        trail = self.get_trail()
        length = self.get_length()
        if position >= length:
            return
        else:
            return trail[position + 1]

    def get_previous_trail(self, position):
        trail = self.get_trail()
        if position < 1:
            return
        else:
            return trail[position - 1]

    def evaluate(self):
        trail_elements = self.get_trail()
        for elements in trail_elements:
            elements.evaluate()

    def agents_count(self):
        trail = self.get_trail()
        tourists_number = 0
        for cell in trail:
            tourists_number += cell.get_tourists_number()
        return tourists_number

    def get_length(self):
        return self.__trail_length

    def get_iter(self):
        return self.__trail_iter

    def get_trail(self):
        return self.__trail

    def get_trail_start(self):
        return self.__start_position

    def get_tourists(self):
        return self.__tourists

    def set_tourists(self, tourists):
        self.__tourists = tourists

    def set_trail(self, elements):
        self.__trail = elements

    def set_length(self, length):
        self.__trail_length = length

    def set_trail_start(self, start):
        self.__start_position = start
