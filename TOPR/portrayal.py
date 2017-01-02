from TOPR.agents import Tourist, TrailElement


def tourist_trial_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Filled": "true"}

    if type(agent) is Tourist:
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1

        probability = agent.get_probability()
        color_specify = round(63*probability)

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
        0: "#0508AC", 1: "#0612AC", 2: "#061EAD", 3: "#0629AE", 4: "#0734AF", 5: "#073FB0", 6: "#074BB1", 7: "#0756B2",
        8: "#0861B2", 9: "#086DB3", 10: "#0879B4", 11: "#0984B5", 12: "#0990B6", 13: "#099CB7", 14: "#0AA8B8",
        15: "#0AB4B9", 16: "#0AB9B3", 17: "#0ABAA8", 18: "#0BBB9E", 19: "#0BBC93", 20: "#0BBD88", 21: "#0CBE7E",
        22: "#0CBF73", 23: "#0CBF73", 24: "#0CC068", 25: "#0DC152", 26: "#0DC247", 27: "#0EC33C", 28: "#0EC431",
        29: "#0EC526", 30: "#0FC61A", 31: "#0FC70F", 32: "#1CC70F", 33: "#28C810", 34: "#34C910", 35: "#40CA11",
        36: "#4DCB11", 37: "#59CC11", 38: "#66CD12", 39: "#73CE12", 40: "#7FCE12", 41: "#8CCF13", 42: "#99D013",
        43: "#A6D113", 44: "#B3D214", 45: "#C0D314", 46: "#CDD415", 47: "#D5CF15", 48: "#D5C415", 49: "#D6B816",
        50: "#D7AD16", 51: "#D8A117", 52: "#D99517", 53: "#DA8917", 54: "#DB7E18", 55: "#DC7218", 56: "#DC6619",
        57: "#DD5A19", 58: "#DE4E19", 59: "#DF421A", 60: "#E0351A", 61: "#E1291B", 62: "#E21D1B", 63: "#E31B26"
    }[x]
