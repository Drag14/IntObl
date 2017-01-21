from mesa import Agent


class Tourist(Agent):
    """Represents a single Tourist cell in the simulation."""

    def __init__(self, unique_id, model, position, moore=True, add_to_schedule=True,
                 probability=1.0, direction="forward", position_in_trail=0, prob_forward=0.9,
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
        contents = self.model.grid.get_cell_list_contents(self._pos)
        is_it_node = False
        trail = None
        for content in contents:
            if type(content) is TrailElement:
                is_it_node = content.get_if_part_of_node()
                if is_it_node:
                    trail = content

        if is_it_node is False:
            neighbors = self.model.grid.get_neighbors(self.get_position(), moore=True, include_center=False)
            if self._direction is "forward":
                for neighbor in neighbors:

                    # if forward tourist can go forward with forward probability
                    if type(neighbor) is TrailElement and neighbor.get_trail_gradient() > self._position_in_trail \
                            and neighbor.get_if_part_of_node() is False:
                        Tourist(unique_id=self.unique_id, model=self.model, position=neighbor.unique_id,
                                position_in_trail=self._position_in_trail + 1, direction="forward",
                                probability=self._probability * self._prob_forward, add_to_schedule=False)

                    # if forward tourist can turn over and go backward with backward probability
                    elif type(neighbor) is TrailElement and neighbor.get_trail_gradient() < self._position_in_trail \
                            and neighbor.get_if_part_of_node() is False:
                        Tourist(unique_id=self.unique_id, model=self.model, position=neighbor.unique_id,
                                position_in_trail=self._position_in_trail - 1, direction="backward",
                                probability=self._probability * self._prob_backward, add_to_schedule=False)

                    elif type(neighbor) is TrailElement and neighbor.get_trail_gradient() > self._position_in_trail \
                            and neighbor.get_if_part_of_node() is True:
                        Tourist(unique_id=self.unique_id, model=self.model, position=neighbor.unique_id,
                                position_in_trail=self._position_in_trail + 1, direction="forward",
                                probability=self._probability * self._prob_forward / 3, add_to_schedule=False)

            elif self._direction is "backward":

                # if backward tourist can turn over again, so go forward with backward probability
                for neighbor in neighbors:
                    if type(neighbor) is TrailElement and neighbor.get_trail_gradient() > self._position_in_trail \
                            and neighbor.get_if_part_of_node() is False:
                        Tourist(unique_id=self.unique_id, model=self.model, position=neighbor.unique_id,
                                position_in_trail=self._position_in_trail + 1, direction="forward",
                                probability=self._probability * self._prob_backward, add_to_schedule=False)

                    # if backward tourist can go backward, but with forward probability (its forward is backward now)
                    elif type(neighbor) is TrailElement and neighbor.get_trail_gradient() < self._position_in_trail \
                            and neighbor.get_if_part_of_node() is False:
                        Tourist(unique_id=self.unique_id, model=self.model, position=neighbor.unique_id,
                                position_in_trail=self._position_in_trail - 1, direction="backward",
                                probability=self._probability * self._prob_forward, add_to_schedule=False)

                    elif type(neighbor) is TrailElement and neighbor.get_trail_gradient() < self._position_in_trail \
                            and neighbor.get_if_part_of_node() is True:
                        Tourist(unique_id=self.unique_id, model=self.model, position=neighbor.unique_id,
                                position_in_trail=self._position_in_trail - 1, direction="backward",
                                probability=self._probability * self._prob_forward / 3, add_to_schedule=False)

            elif self._direction is "stay":
                for neighbor in neighbors:

                    # if tourist stayed he can go forward again
                    if type(neighbor) is TrailElement and neighbor.get_trail_gradient() > self._position_in_trail \
                            and neighbor.get_if_part_of_node() is False:
                        Tourist(unique_id=self.unique_id, model=self.model, position=neighbor.unique_id,
                                position_in_trail=self._position_in_trail + 1, direction="forward",
                                probability=self._probability * self._prob_forward, add_to_schedule=False)

                    # if tourist stayed he can go backward again
                    elif type(neighbor) is TrailElement and neighbor.get_trail_gradient() < self._position_in_trail \
                            and neighbor.get_if_part_of_node() is False:
                        Tourist(unique_id=self.unique_id, model=self.model, position=neighbor.unique_id,
                                position_in_trail=self._position_in_trail - 1, direction="backward",
                                probability=self._probability * self._prob_backward, add_to_schedule=False)

        # What happens when tourist is in the node - depending on which part of node and which direction is he going.
        else:
            direction = trail.get_which_dir_node()

            if direction == 'left' and self._direction == 'forward':
                x, y = trail.unique_id
                Tourist(unique_id=self.unique_id, model=self.model, position=(x - 1, y - 1),
                        position_in_trail=self._position_in_trail + 1, direction="forward",
                        probability=self._probability * self._prob_forward, add_to_schedule=False)
                Tourist(unique_id=self.unique_id, model=self.model, position=(x + 1, y + 1),
                        position_in_trail=self._position_in_trail - 1, direction="backward",
                        probability=self._probability * self._prob_backward, add_to_schedule=False)

            elif direction == 'right' and self._direction == 'forward':
                x, y = trail.unique_id
                Tourist(unique_id=self.unique_id, model=self.model, position=(x + 1, y - 1),
                        position_in_trail=self._position_in_trail + 1, direction="forward",
                        probability=self._probability * self._prob_forward, add_to_schedule=False)
                Tourist(unique_id=self.unique_id, model=self.model, position=(x - 1, y + 1),
                        position_in_trail=self._position_in_trail - 1, direction="backward",
                        probability=self._probability * self._prob_backward, add_to_schedule=False)

            elif direction == 'middle' and self._direction == 'forward':
                x, y = trail.unique_id
                Tourist(unique_id=self.unique_id, model=self.model, position=(x, y - 1),
                        position_in_trail=self._position_in_trail + 1, direction="forward",
                        probability=self._probability * self._prob_forward, add_to_schedule=False)
                Tourist(unique_id=self.unique_id, model=self.model, position=(x, y + 1),
                        position_in_trail=self._position_in_trail - 1, direction="backward",
                        probability=self._probability * self._prob_backward, add_to_schedule=False)

            elif direction == 'left' and self._direction == 'backward':
                x, y = trail.unique_id
                Tourist(unique_id=self.unique_id, model=self.model, position=(x - 1, y - 1),
                        position_in_trail=self._position_in_trail + 1, direction="forward",
                        probability=self._probability * self._prob_backward, add_to_schedule=False)
                Tourist(unique_id=self.unique_id, model=self.model, position=(x + 1, y + 1),
                        position_in_trail=self._position_in_trail - 1, direction="backward",
                        probability=self._probability * self._prob_forward, add_to_schedule=False)

            elif direction == 'right' and self._direction == 'backward':
                x, y = trail.unique_id
                Tourist(unique_id=self.unique_id, model=self.model, position=(x + 1, y - 1),
                        position_in_trail=self._position_in_trail + 1, direction="forward",
                        probability=self._probability * self._prob_backward, add_to_schedule=False)
                Tourist(unique_id=self.unique_id, model=self.model, position=(x - 1, y + 1),
                        position_in_trail=self._position_in_trail - 1, direction="backward",
                        probability=self._probability * self._prob_forward, add_to_schedule=False)

            elif direction == 'middle' and self._direction == 'backward':
                x, y = trail.unique_id
                Tourist(unique_id=self.unique_id, model=self.model, position=(x, y - 1),
                        position_in_trail=self._position_in_trail + 1, direction="forward",
                        probability=self._probability * self._prob_backward, add_to_schedule=False)
                Tourist(unique_id=self.unique_id, model=self.model, position=(x, y + 1),
                        position_in_trail=self._position_in_trail - 1, direction="backward",
                        probability=self._probability * self._prob_forward, add_to_schedule=False)

        # tourist in the place we start - we assume it's the agents that stays,
        # so we give him probability of self.prob*stay_prob
        self._probability *= self._prob_stay
        self._direction = 'stay'

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

    def __init__(self, unique_id, model, trail_gradient, part_of_node=False, which_dir_node=None):
        """
        Create a cell of trail, at the given x, y position.
        """
        super().__init__(unique_id, model)

        self.trail_gradient = trail_gradient
        self._part_of_node = part_of_node
        self._which_dir_node = which_dir_node
        if part_of_node:
            self._which_dir_node = which_dir_node

        self.model.grid.place_agent(self, unique_id)

    def advance(self):
        contents = self.model.grid.get_cell_list_contents(self.unique_id)

        tourists_stayed = []
        tourists_forward = []
        tourists_backward = []
        tourist_dictionary = {"tourist_stayed": tourists_stayed, "tourists_forward": tourists_forward,
                              "tourists_backward": tourists_backward}

        # separate tourists inside of cell in reference to direction
        for content in contents:
            if type(content) is TrailElement:
                pass
            if type(content) is Tourist:
                if content.get_direction() == 'stay':
                    tourists_stayed.append(content)
                elif content.get_direction() == 'forward':
                    tourists_forward.append(content)
                elif content.get_direction() == 'backward':
                    tourists_backward.append(content)

        # create resultant probability of tourists that are going in the same direction after every tourist checked -
        # delete it from the grid - will be replaced by one tourist with resultant_probability
        for key, values in tourist_dictionary.items():
            if len(values) > 1:
                resultant_probability = 0
                unique_id = None
                tourist_direction = None
                position_in_trail = None
                position = []
                flag = 0
                for tourist in values:
                    if flag == 0:
                        tourist_direction = tourist.get_direction()
                        unique_id = tourist.unique_id
                        position = tourist.get_position()
                        position_in_trail = tourist.get_position_in_trail()
                        flag += 1
                    resultant_probability += tourist.get_probability()
                    self.model.grid._remove_agent(position, tourist)

                if resultant_probability > self.model.maximum_probability:
                    self.model.maximum_probability = resultant_probability

                if resultant_probability < self.model.minimum_probability:
                    self.model.minimum_probability = resultant_probability

                Tourist(unique_id=unique_id, model=self.model, position=position,
                        position_in_trail=position_in_trail, direction=tourist_direction,
                        probability=resultant_probability, add_to_schedule=True)
            else:
                for value in values:
                    self.model.schedule_tourists.add(value)

    def get_geo_pos(self):
        return self.unique_id

    def get_trail_gradient(self):
        return self.trail_gradient

    def get_if_part_of_node(self):
        return self._part_of_node

    def get_which_dir_node(self):
        return self._which_dir_node


class TrailNode:
    def __init__(self, unique_id, model, contiguous_element, left=True, middle=True, right=True):
        self.model = model
        self.node_left = None
        self.node_middle = None
        self.node_right = None
        self.elements = []
        self.gradient = 0

        (x, y) = unique_id
        (x_prev, y_prev) = contiguous_element.get_geo_pos()
        self.gradient = contiguous_element.get_trail_gradient() + 1

        elements = []
        if x_prev == x and y_prev >= y:
            if left:
                self.node_left = TrailElement(unique_id=(x - 1, y - 1), model=model, trail_gradient=self.gradient,
                                              part_of_node=True, which_dir_node='left')
            if right:
                self.node_right = TrailElement((x + 1, y - 1), model, trail_gradient=self.gradient,
                                               part_of_node=True, which_dir_node='right')
            if middle:
                self.node_middle = TrailElement((x, y - 1), model, trail_gradient=self.gradient,
                                                part_of_node=True, which_dir_node='middle')
            for element in elements:
                model.grid.place_agent(element, element.get_geo_pos())

    def extend_node(self, left, middle, right):
        if self.node_left is not None:
            (x, y) = self.node_left.get_geo_pos()
            y -= 1
            x -= 1
            for i in range(1, left):
                if self.model.grid.is_cell_empty((x, y)) is False:
                    break
                else:
                    self.node_left = TrailElement(unique_id=(x, y), model=self.model,
                                                  trail_gradient=self.gradient + i)
                    self.elements.append(self.node_left)
                    y -= 1
                    x -= 1

        if self.node_middle is not None:
            (x, y) = self.node_middle.get_geo_pos()
            y -= 1
            for i in range(1, middle):
                if self.model.grid.is_cell_empty((x, y)) is False:
                    break
                else:
                    self.node_middle = TrailElement(unique_id=(x, y), model=self.model,
                                                    trail_gradient=self.gradient + i)
                    self.elements.append(self.node_middle)
                    y -= 1

        if self.node_right is not None:
            (x, y) = self.node_right.get_geo_pos()
            y -= 1
            x += 1
            for i in range(1, right):
                if self.model.grid.is_cell_empty((x, y)) is False:
                    break
                else:
                    self.node_right = TrailElement(unique_id=(x, y), model=self.model,
                                                   trail_gradient=self.gradient + i)
                    self.elements.append(self.node_right)
                    y -= 1
                    x += 1


class Trail:
    """Represents whole Trail in the simulation - for easier manipulation"""

    def __init__(self, model):
        self.model = model
        self._start_position = []
        self.trail = []
        self.trail_for_two()
        # self.trail_for_three_tourists()

    def trail_for_two(self):
        x = [20, 60]
        y = 190
        for i in range(0, 2):
            trail_element = TrailElement(unique_id=(x[i], y), model=self.model, trail_gradient=0)
            self.set_trail_start(trail_element)
            self.trail.append(trail_element)
            self.model.schedule_trail_elements.add(trail_element)
            start_tourist = Tourist(position=(x[i], y), unique_id=i, model=self.model)
            self.model.grid.place_agent(start_tourist, (x[i], y))

        trail_indicator = []
        for tourist in self._start_position:
            (x, y) = tourist.get_geo_pos()
            trail_element = None
            for j in range(1, 20):
                trail_element = TrailElement(unique_id=(x, y - j), model=self.model, trail_gradient=j)
                if trail_element is not None:
                    self.trail.append(trail_element)
            if trail_element is not None:
                trail_indicator.append(trail_element)

        trail_node1 = TrailNode(unique_id=trail_indicator[0].get_geo_pos(), model=self.model,
                                contiguous_element=trail_indicator[0], left=False, middle=False)
        self.add_node_to_trail(trail_node1)

        trail_node1.extend_node(0, 0, 20)

        for element in trail_node1.elements:
            self.trail.append(element)

        grad = trail_node1.node_right.get_trail_gradient()
        x, y = trail_node1.node_right.get_geo_pos()
        for j in range(1, 20):
            trail_element = TrailElement(unique_id=(x, y - j), model=self.model, trail_gradient=grad + j)
            if trail_element is not None:
                self.trail.append(trail_element)

        trail_node2 = TrailNode(unique_id=trail_indicator[1].get_geo_pos(), model=self.model,
                                contiguous_element=trail_indicator[1], right=False, middle=False)
        self.add_node_to_trail(trail_node2)
        trail_node2.extend_node(20, 0, 0)

        for element in trail_node2.elements:
            self.trail.append(element)

    def trail_for_three_tourists(self):
        x = [20, 100, 160]
        y = 190
        for i in range(0, 3):
            trail_element = TrailElement(unique_id=(x[i], y), model=self.model, trail_gradient=0)
            self.set_trail_start(trail_element)
            self.trail.append(trail_element)
            self.model.schedule_trail_elements.add(trail_element)
            start_tourist = Tourist(position=(x[i], y), unique_id=i, model=self.model,
                                    probability=1)
            self.model.grid.place_agent(start_tourist, (x[i], y))

        trail_indicator = []
        for tourist in self._start_position:
            (x, y) = tourist.get_geo_pos()
            trail_element = None
            for j in range(1, 20):
                trail_element = TrailElement(unique_id=(x, y - j), model=self.model, trail_gradient=j)
                if trail_element is not None:
                    self.trail.append(trail_element)

            trail_indicator.append(trail_element)

        trail_node1 = TrailNode(unique_id=trail_indicator[0].get_geo_pos(), model=self.model,
                                contiguous_element=trail_indicator[0], left=True, middle=False, right=True)
        self.add_node_to_trail(trail_node1)
        trail_node1.extend_node(left=15, middle=0, right=40)

        for element in trail_node1.elements:
            self.trail.append(element)

        grad = trail_node1.node_right.get_trail_gradient()
        x, y = trail_node1.node_right.get_geo_pos()
        trail_element = None
        for j in range(1, 20):
            trail_element = TrailElement(unique_id=(x, y - j), model=self.model, trail_gradient=grad + j)
            if trail_element is not None:
                self.trail.append(trail_element)

        trail_node2 = TrailNode(unique_id=trail_indicator[1].get_geo_pos(), model=self.model,
                                contiguous_element=trail_indicator[1], left=True, middle=True, right=False)
        self.add_node_to_trail(trail_node2)
        trail_node2.extend_node(left=40, middle=170, right=0)

        for element in trail_node2.elements:
            self.trail.append(element)

        trail_node12 = TrailNode(unique_id=trail_element.get_geo_pos(), model=self.model,
                                 contiguous_element=trail_element, left=True, middle=True, right=True)
        self.add_node_to_trail(trail_node12)
        trail_node12.extend_node(left=40, middle=40, right=40)

        for element in trail_node12.elements:
            self.trail.append(element)

        grad = trail_node12.node_left.get_trail_gradient()
        x, y = trail_node12.node_left.get_geo_pos()
        for j in range(1, 20):
            trail_element = TrailElement(unique_id=(x, y - j), model=self.model, trail_gradient=grad + j)
            if trail_element is not None:
                self.trail.append(trail_element)

        trail_node123 = TrailNode(unique_id=trail_element.get_geo_pos(), model=self.model,
                                  contiguous_element=trail_element, left=False, middle=False, right=True)
        self.add_node_to_trail(trail_node123)
        trail_node123.extend_node(left=0, middle=0, right=50)

        for element in trail_node123.elements:
            self.trail.append(element)

        grad = trail_node123.node_right.get_trail_gradient()
        x, y = trail_node123.node_right.get_geo_pos()
        for j in range(1, 31):
            trail_element = TrailElement(unique_id=(x + j, y), model=self.model, trail_gradient=grad + j)
            self.trail.append(trail_element)

        trail_node122 = TrailNode(unique_id=trail_node12.node_middle.get_geo_pos(), model=self.model,
                                  contiguous_element=trail_node12.node_middle, left=False, middle=False, right=True)
        self.add_node_to_trail(trail_node12)
        trail_node122.extend_node(left=0, middle=0, right=40)

        for element in trail_node122.elements:
            self.trail.append(element)

        trail_node3 = TrailNode(unique_id=trail_indicator[2].get_geo_pos(), model=self.model,
                                contiguous_element=trail_indicator[2], left=True, middle=False, right=True)
        self.add_node_to_trail(trail_node3)
        trail_node3.extend_node(left=60, middle=0, right=20)

        for element in trail_node3.elements:
            self.trail.append(element)

        grad = trail_node3.node_right.get_trail_gradient()
        x, y = trail_node3.node_right.get_geo_pos()
        for j in range(1, 40):
            trail_element = TrailElement(unique_id=(x, y-j), model=self.model, trail_gradient=grad + j)
            self.trail.append(trail_element)

        trail_node32 = TrailNode(unique_id=trail_element.get_geo_pos(), model=self.model,
                                 contiguous_element=trail_element, left=True, middle=True, right=False)
        self.add_node_to_trail(trail_node32)
        trail_node3.extend_node(left=80, middle=113, right=0)

        for element in trail_node3.elements:
            self.trail.append(element)

    # def random_trail_for_few_tourists(self, tourist_number):
    #     for i in range(0, tourist_number):
    #         x = random.randrange(round(i * self.model.width / tourist_number),
    #                              round((i + 1) * self.model.width / tourist_number))
    #         y = random.randrange(self.model.height - 10, self.model.height)
    #         trail_element = TrailElement(unique_id=(x, y), model=self.model, trail_gradient=0)
    #         self.set_trail_start(trail_element)
    #         self.trail.append(trail_element)
    #         self.model.schedule_trail_elements.add(trail_element)
    #         start_tourist = Tourist(position=(x, y), unique_id=tourist_number, model=self.model,
    #                                 probability=1)
    #         self.model.grid.place_agent(start_tourist, (x, y))
    #
    #     trail_indicator = []
    #     for tourist in self._start_position:
    #         (x, y) = tourist.get_geo_pos()
    #         trail_element = None
    #         for j in range(1, 20):
    #             trail_element = TrailElement(unique_id=(x, y), model=self.model, trail_gradient=j)
    #             self.trail.append(trail_element)
    #             y -= 1
    #         trail_indicator.append(trail_element)
    #
    #     trail_node = TrailNode(unique_id=trail_indicator[0].get_geo_pos(), model=self.model,
    #                            contiguous_element=trail_indicator[0])
    #     self.add_node_to_trail(trail_node)
    #     elements, trail_left, trail_middle, trail_right = self.node_crossing(trail_node, left=5,
    #                                                                          middle=10, right=50)
    #     for element in elements:
    #         self.trail.append(element)
    #
    #     trail_node = TrailNode(unique_id=trail_indicator[1].get_geo_pos(), model=self.model,
    #                            contiguous_element=trail_indicator[1])
    #     self.add_node_to_trail(trail_node)
    #     elements, trail_left, trail_middle, trail_right = self.node_crossing(trail_node, left=100,
    #                                                                          middle=20, right=0)
    #     for element in elements:
    #         self.trail.append(element)

    def add_node_to_trail(self, node):
        if node.node_left is not None:
            self.trail.append(node.node_left)
        elif node.node_right is not None:
            self.trail.append(node.node_right)
        elif node.node_middle is not None:
            self.trail.append(node.node_middle)

    def get_trail_start(self):
        return self._start_position

    def set_trail_start(self, start):
        self._start_position.append(start)
