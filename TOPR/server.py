from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from TOPR.portrayal import tourist_trial_portrayal
from TOPR.model import TOPRAction
from TOPR.config import width, height

canvas_element = CanvasGrid(tourist_trial_portrayal, grid_width=width, grid_height=height)

server = ModularServer(TOPRAction, [canvas_element], "TOPRAction")
