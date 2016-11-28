from TOPR.agents import Tourist, TrailElement
import re


def tourist_trial_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Filled": "true"}

    if type(agent) is Tourist:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "Black"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1

    elif type(agent) is TrailElement:
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

        (x, y) = agent.get_geo_pos()
        probability = agent.get_probability()
        portrayal["x"] = x
        portrayal["y"] = y

        color_specify = round(probability*10)

        color = color_def(color_specify)
        portrayal["Color"] = color
        return portrayal

    return portrayal


def color_def(x):
    return {
        10: "#E51C00", 9: "#E06700", 8: "#DCAE00", 7: "#BDD800", 6: "#72D400",
        5: "#2BCF00", 4: "#00CB19", 3: "#00C75B", 2: "#00C39A", 1: "#00A6BF"
    }[x]
