from TOPR.agents import Tourist, TrailElement
import re


def tourist_trial_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Filled": "true"}

    if type(agent) is Tourist:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1

        probability = agent.get_probability()

        color_specify = round(probability * 10)

        color = color_def(color_specify)
        portrayal["Color"] = color

    elif type(agent) is TrailElement:
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 0
        portrayal["Color"] = "black"
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


def color_def(x):
    return {
        10: "#E51C00", 9: "#E06700", 8: "#DCAE00", 7: "#BDD800", 6: "#72D400",
        5: "#2BCF00", 4: "#00CB19", 3: "#00C75B", 2: "#00C39A", 1: "#00A6BF",
        0: "#00A6BF"
    }[x]
