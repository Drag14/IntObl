from TOPR.agents import Tourist, TrailElement
import math


def tourist_trial_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Filled": "true"}

    if type(agent) is Tourist:
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1

        maximum = agent.model.maximum_probability
        minimum = agent.model.minimum_probability
        probability = agent.get_probability()
        r, g, b = floatRgb(probability, minimum, maximum)
        portrayal["Color"] = '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))

    elif type(agent) is TrailElement:
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 0
        portrayal["Color"] = "black"
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


def floatRgb(mag, cmin, cmax):
    """ Return a tuple of floats between 0 and 1 for R, G, and B. """
    # Normalize to 0-1
    try:
        x = float(mag - cmin) / (cmax - cmin)
    except ZeroDivisionError:
        x = 0.5  # cmax == cmin
    blue = min((max((4 * (0.75 - x), 0.)), 1.))
    red = min((max((4 * (x - 0.25), 0.)), 1.))
    green = min((max((4 * math.fabs(x - 0.5) - 1., 0.)), 1.))
    return red, green, blue
