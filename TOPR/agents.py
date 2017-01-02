from mesa import Agent
import random


class Tourist(Agent):
    """Represents a single Tourist cell in the simulation."""

    def __init__(self, unique_id, model, position, moore=True, add_to_schedule=True,
                 probability=0.0, direction="forward", position_in_trail=0, prob_forward=0.9,
                 prob_backward=0.05, prob_stay=0.05):

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
        self._pos = position
        self._position_in_trail = position_in_trail
        self._prob_forward = prob_forward
        self._prob_backward = prob_backward
        self._prob_stay = prob_stay
        self._probability = probability
        self._direction = direction
        if add_to_schedule:
            self.model.schedule_tourists.add(self)

        self.model.grid.place_agent(self, position)

    def advance(self):
        """
        Step one cell in any allowable direction with concrete probability distribution.
        0.9 - forward, 0.05 - return, 0.05 - stay in place
        """
        neighbors = self.model.grid.get_neighbors(self.get_position(), moore=True, include_center=True)
        if self._direction is "forward":
            for neighbor in neighbors:
                if type(neighbor) is TrailElement and neighbor.get_trail_gradient() > self._position_in_trail:
                    neighbor.set_prob_upper(self.get_prob_forward() * self.get_probability())
                elif type(neighbor) is TrailElement and neighbor.get_trail_gradient() < self._position_in_trail:
                    neighbor.set_prob_lower(self.get_prob_backward() * self.get_probability())
                elif type(neighbor) is TrailElement and neighbor.get_trail_gradient() == self._position_in_trail:
                    neighbor.set_prob_middle(self._prob_stay * self.get_probability())
        else:
            for neighbor in neighbors:
                if type(neighbor) is TrailElement and neighbor.get_trail_gradient() < self._position_in_trail:
                    neighbor.set_prob_upper(self.get_prob_forward() * self.get_probability())
                elif type(neighbor) is TrailElement and neighbor.get_trail_gradient() > self._position_in_trail:
                    neighbor.set_prob_lower(self.get_prob_backward() * self.get_probability())
                elif type(neighbor) is TrailElement and neighbor.get_trail_gradient() == self._position_in_trail:
                    neighbor.set_prob_middle(self._prob_stay * self.get_probability())

    def get_position_in_trail(self):
        return self._position_in_trail

    def set_position_in_trail(self, pos):
        self._position_in_trail = pos

    def get_position(self):
        return self._pos

    def set_position(self, pos):
        self._pos = pos

    def get_probability(self):
        return self._probability

    def set_probability(self, probability):
        if self._probability == 0:
            self._probability = probability
        else:
            self._probability *= probability

    def get_prob_forward(self):
        return self._prob_forward

    def get_prob_stay(self):
        return self._prob_stay

    def get_prob_backward(self):
        return self._prob_backward

    def get_direction(self):
        return self._direction


class TrailElement(Agent):
    """Represents a single Trail cell in the simulation."""

    def __init__(self, unique_id, model, trail_gradient, part_of_node=False, probability_upper=0, probability_middle=0,
                 probability_lower=0):
        """
        Create a cell of trail, at the given x, y position.
        """
        super().__init__(unique_id, model)

        self._probability_upper = probability_upper
        self._probability_middle = probability_middle
        self._probability_lower = probability_lower

        self.trail_gradient = trail_gradient
        self._part_of_node = part_of_node
        self.model.grid.place_agent(self, unique_id)

    def advance(self):
        resultant_probability = self._probability_upper + self._probability_middle + self._probability_lower
        Tourist(position=self.get_geo_pos(), unique_id=1, model=self.model,
                add_to_schedule=True, position_in_trail=self.get_trail_gradient(),
                direction="forward", probability=resultant_probability)

        Tourist(position=self.get_geo_pos(), unique_id=1, model=self.model,
                add_to_schedule=True, position_in_trail=self.get_trail_gradient(),
                direction="backward", probability=resultant_probability)

    def get_geo_pos(self):
        return self.unique_id

    def get_trail_gradient(self):
        return self.trail_gradient

    def get_if_part_of_node(self):
        return self._part_of_node

    def set_prob_upper(self, probability):
        self._probability_upper = probability

    def set_prob_middle(self, probability):
        self._probability_middle = probability

    def set_prob_lower(self, probability):
        self._probability_lower = probability

    def get_prob_upper(self):
        return self._probability_upper

    def get_prob_middle(self):
        return self._probability_middle

    def get_prob_lower(self):
        return self._probability_lower


class TrailNode:
    def __init__(self, unique_id, model, contiguous_element):
        self.model = model
        self.node_left = None
        self.node_middle = None
        self.node_right = None

        (x, y) = unique_id
        (x_prev, y_prev) = contiguous_element.get_geo_pos()
        trail_gradient = contiguous_element.get_trail_gradient() + 1

        elements = []
        if x_prev == x and y_prev >= y:
            self.node_left = TrailElement(unique_id=(x - 1, y), model=model, trail_gradient=trail_gradient,
                                          part_of_node=True)

            self.node_middle = TrailElement((x, y), model, trail_gradient=trail_gradient,
                                            part_of_node=True)

            self.node_right = TrailElement((x + 1, y), model, trail_gradient=trail_gradient,
                                           part_of_node=True)

            for element in elements:
                model.grid.place_agent(element, element.get_geo_pos())


class Trail:
    """Represents whole Trail in the simulation - for easier manipulation"""

    def __init__(self, model, tourists=1):
        self.model = model
        self._trail_length = 0
        self._start_position = None
        self._tourists = tourists
        self.trail = []
        self.test_trail()

    def test_trail(self):
        length = 0
        x = random.randrange(self.model.width / 2 - 20, self.model.width / 2 + 20)
        y = random.randrange(self.model.height - 10, self.model.height)
        self.set_trail_start((x, y))

        trail_element = TrailElement(unique_id=(x, y), model=self.model, trail_gradient=0)
        self.trail.append(trail_element)
        self.model.schedule_trail_elements.add(trail_element)
        start_tourist = Tourist(position=self.get_trail_start(), unique_id=1, model=self.model, probability=1)
        self.model.grid.place_agent(start_tourist, self.get_trail_start())

        length += 1

        for i in range(1, 20):
            trail_element = TrailElement(unique_id=(x, y), model=self.model, trail_gradient=i)
            self.trail.append(trail_element)
            y -= 1
            length += 1

        trail_node1 = TrailNode(unique_id=(x, y), model=self.model, contiguous_element=trail_element)
        self.trail.append(trail_node1.node_left)
        self.trail.append(trail_node1.node_right)
        self.trail.append(trail_node1.node_middle)
        elements, trail_left, trail_middle, trail_right = self.node_crossing(trail_node1, left=30, middle=20, right=60)
        for element in elements:
            self.trail.append(element)

        trail_node2 = TrailNode(unique_id=trail_left.get_geo_pos(), model=self.model, contiguous_element=trail_left)
        self.trail.append(trail_node2.node_left)
        self.trail.append(trail_node2.node_right)
        self.trail.append(trail_node2.node_middle)
        elements, trail_left2, trail_middle2, trail_right2 = self.node_crossing(trail_node2, left=15, middle=15,
                                                                                right=35)
        for element in elements:
            self.trail.append(element)

        # TrailNode3 = TrailNode(unique_id=trail_middle.get_geo_pos(), model=self.model,
        #                        contiguous_element=trail_middle)

        # trail_left3, trail_middle3, trail_right3 = self.node_crossing(TrailNode3, left=40, middle=100, right=0)
        #
        # TrailNode4 = TrailNode(unique_id=trail_right2.get_geo_pos(), model=self.model,
        #                          contiguous_element=trail_right2)
        # trail_left5, trail_middle5, trail_right5 = self.node_crossing(TrailNode4, left=40, middle=55, right=0)
        #
        # TrailNode4 = TrailNode(unique_id=trail_right.get_geo_pos(), model=self.model,
        #                          contiguous_element=trail_right)
        # trail_left4, trail_middle4, trail_right4 = self.node_crossing(TrailNode4, left=60, middle=20, right=0)
        self.set_length(length)

    def node_crossing(self, trail_node, left=20, middle=20, right=20):
        trail_left = None
        trail_middle = None
        trail_right = None
        trail_gradient = trail_node.node_left.get_trail_gradient()
        elements = []
        (x, y) = trail_node.node_left.get_geo_pos()
        y -= 1
        x -= 1
        for i in range(1, left):
            if self.model.grid.is_cell_empty((x, y)) is False:
                break
            else:
                trail_left = TrailElement(unique_id=(x, y), model=self.model,
                                          trail_gradient=trail_gradient + i)
                elements.append(trail_left)
                y -= 1
                x -= 1

        (x, y) = trail_node.node_middle.get_geo_pos()
        y -= 1
        for i in range(1, middle):
            if self.model.grid.is_cell_empty((x, y)) is False:
                break
            else:
                trail_middle = TrailElement(unique_id=(x, y), model=self.model,
                                            trail_gradient=trail_gradient + i)
                elements.append(trail_middle)
                y -= 1

        (x, y) = trail_node.node_right.get_geo_pos()
        y -= 1
        x += 1
        for i in range(1, right):
            if self.model.grid.is_cell_empty((x, y)) is False:
                break
            else:
                trail_right = TrailElement(unique_id=(x, y), model=self.model,
                                           trail_gradient=trail_gradient + i)
                elements.append(trail_right)
                y -= 1
                x += 1

        return elements, trail_left, trail_middle, trail_right

    def get_length(self):
        return self._trail_length

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
