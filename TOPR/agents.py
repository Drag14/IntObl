from mesa import Agent
import random


class Tourist(Agent):
    """Represents a single Tourist cell in the simulation."""

    def __init__(self, unique_id, model, position, energy=1, moore=True, add_to_schedule=True,
                 probability=0.0, position_in_trail=0, prob_forward=0.9,
                 prob_backward=0.09, prob_stay=0.01):

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
        neighbors = self.model.grid.get_neighbors(self.get_position(), moore=True)
        my_position = self.get_position()
        for neighbor in neighbors:

            if type(neighbor) is TrailElement and neighbor.get_trail_gradient() > self._position_in_trail:
                tourist_forward = Tourist(position=neighbor.get_geo_pos(), unique_id=1, model=self.model,
                                          add_to_schedule=False, position_in_trail=neighbor.get_trail_gradient(),
                                          probability=self.get_prob_forward())
                neighbor.add_tourist(tourist_forward)
                self.model.grid.place_agent(tourist_forward, neighbor.get_geo_pos())

            elif type(neighbor) is TrailElement and neighbor.get_trail_gradient() < self._position_in_trail:
                tourist_back = Tourist(position=neighbor.get_geo_pos(), unique_id=1, model=self.model,
                                       add_to_schedule=False, position_in_trail=neighbor.get_trail_gradient(),
                                       probability=self.get_prob_backward())
                neighbor.add_tourist(tourist_back)
                self.model.grid.place_agent(tourist_back, neighbor.get_geo_pos())

            # elif type(neighbor) is TrailElement and neighbor.get_if_part_of_node():
            #     tourist_back = Tourist(position=neighbor.get_geo_pos(), unique_id=1, model=self.model,
            #                            add_to_schedule=False, position_in_trail=neighbor.get_trail_gradient(),
            #                            probability=self.get_prob_backward())
            #     neighbor.add_tourist(tourist_back)
            #     self.model.grid.place_agent(tourist_back, neighbor.get_geo_pos())

            # if neighbor is type(Trail_Node) and neighbor.node_left.get_trail_gradient() > self._position_in_trail:
            #     tourist_left = Tourist(position=neighbor.get_geo_pos(), unique_id=1, model=self.model,
            #                            add_to_schedule=False, position_in_trail=neighbor.get_trail_gradient(),
            #                            probability=self.get_prob_forward())
            #     tourist_middle = Tourist(position=neighbor.get_geo_pos(), unique_id=1, model=self.model,
            #                              add_to_schedule=False, position_in_trail=neighbor.get_trail_gradient(),
            #                              probability=self.get_prob_forward())
            #     tourist_right = Tourist(position=neighbor.get_geo_pos(), unique_id=1, model=self.model,
            #                             add_to_schedule=False, position_in_trail=neighbor.get_trail_gradient(),
            #                             probability=self.get_prob_forward())

                # if self._position_in_trail < self.model.trail.get_length() - 1:
                #     geo_position = self.model.trail.trail[self._position_in_trail + 1].get_geo_pos()
                #
                #     tourist_forward = Tourist(position=geo_position, unique_id=1, model=self.model,
                #                               add_to_schedule=False, position_in_trail=self._position_in_trail + 1,
                #                               probability=self.get_prob_forward())
                #
                #     self.model.trail.trail[self._position_in_trail].add_tourist(tourist_forward)
                #
                #     self.model.grid.place_agent(tourist_forward, geo_position)
                #
                # if self._position_in_trail > 1:
                #     geo_position = self.model.trail.trail[self._position_in_trail - 1].get_geo_pos()
                #
                #     tourist_back = Tourist(position=geo_position, unique_id=1, model=self.model,
                #                            add_to_schedule=False, position_in_trail=self._position_in_trail - 1,
                #                            probability=self.get_prob_backward())
                #
                #     self.model.grid.place_agent(tourist_back, geo_position)

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
    def __init__(self, unique_id, model, trail_gradient, part_of_node=False):
        """
        Create a cell of trail, at the given x, y position.
        """
        super().__init__(unique_id, model)
        self._tourists = []
        self._trail_gradient = trail_gradient
        self._part_of_node = part_of_node
        self.model.schedule_trail_elements.add(self)
        self.model.grid.place_agent(self, unique_id)

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

    def get_trail_gradient(self):
        return self._trail_gradient

    def get_if_part_of_node(self):
        return self._part_of_node


class Trail_Node:
    def __init__(self, unique_id, model, contiguous_element):
        self.model = model
        self.node_left = None
        self.node_middle = None
        self.node_right = None

        (x, y) = unique_id
        (x_prev, y_prev) = contiguous_element.get_geo_pos()
        trail_gradient = contiguous_element.get_trail_gradient()+1

        elements = []
        if x_prev == x and y_prev >= y:
            self.node_left = TrailElement(unique_id=(x - 1, y), model=model, trail_gradient=trail_gradient,
                                          part_of_node=True)
            elements.append(self.node_left)
            self.node_middle = TrailElement((x, y), model, trail_gradient=trail_gradient,
                                            part_of_node=True)
            elements.append(self.node_middle)
            self.node_right = TrailElement((x + 1, y), model, trail_gradient=trail_gradient,
                                           part_of_node=True)
            elements.append(self.node_right)

            for element in elements:
                model.schedule_trail_elements.add(element)
                model.grid.place_agent(self.node_left, self.node_left.get_geo_pos())


class Trail:
    def __init__(self, model, tourists=1):
        self.model = model
        self._trail_length = 0
        self._start_position = None
        self._tourists = tourists

        self.test_trail()

    def test_trail(self):
        length = 0
        x = random.randrange(self.model.width / 2 - 20, self.model.width / 2 + 20)
        y = random.randrange(self.model.height - 10, self.model.height)
        self.set_trail_start((x, y))

        trail_element = TrailElement(unique_id=(x, y), model=self.model, trail_gradient=0)
        self.model.schedule_trail_elements.add(trail_element)
        length += 1

        for i in range(1, 20):
            trail_element = TrailElement(unique_id=(x, y), model=self.model, trail_gradient=i)
            self.model.schedule_trail_elements.add(trail_element)
            y -= 1
            length += 1

        trail_node1 = Trail_Node(unique_id=(x, y), model=self.model, contiguous_element=trail_element)
        trail_left, trail_middle, trail_right = self.node_crossing(trail_node1, left=30, middle=20, right=10)

        trail_node2 = Trail_Node(unique_id=trail_left.get_geo_pos(), model=self.model, contiguous_element=trail_left)
        trail_left2, trail_middle2, trail_right2 = self.node_crossing(trail_node2, left=15, middle=15, right=35)

        trail_node3 = Trail_Node(unique_id=trail_middle.get_geo_pos(), model=self.model,
                                 contiguous_element=trail_middle)
        trail_left3, trail_middle3, trail_right3 = self.node_crossing(trail_node3, left=40, middle=100, right=0)

        self.model.grid.place_agent(Tourist(position=self.get_trail_start(), unique_id=1, model=self.model),
                                    self.get_trail_start())

        self.set_length(length)

    def node_crossing(self, trail_node, left=20, middle=20, right=20):
        trail_left = None
        trail_middle = None
        trail_right = None
        trail_gradient = trail_node.node_left.get_trail_gradient()

        (x, y) = trail_node.node_left.get_geo_pos()
        y -= 1
        x -= 1
        for i in range(1, left):
            if self.model.grid.is_cell_empty((x, y)) is False:
                break
            else:
                trail_left = TrailElement(unique_id=(x, y), model=self.model,
                                          trail_gradient=trail_gradient + i)
                self.model.schedule_trail_elements.add(trail_left)
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
                self.model.schedule_trail_elements.add(trail_middle)
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
                self.model.schedule_trail_elements.add(trail_right)
                y -= 1
                x += 1

        return trail_left, trail_middle, trail_right

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
