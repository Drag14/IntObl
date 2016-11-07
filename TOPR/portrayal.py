from TOPR.agents import Tourist, Trail


def tourist_trial_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Filled": "true"}

    if type(agent) is Tourist:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "Red"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1

    elif type(agent) is Trail:
        portrayal["Color"] = "Black"
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal