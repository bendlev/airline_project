# date: 08 nov 2022
# author: @bendlev
# purpose: Airport class, used for visualization

# students will have to code this themselves to suit airport_graph.txt

from cs1lib import *
from math import sqrt

class Airport:

    def __init__(self, iata, name, city, lat, long) -> None:
        self.iata = iata
        self.name = name
        self.city = city
        self.lat = float(lat)
        self.long = float(long)

        

        self.RADIUS = 2

        self.neighbors = []
        self.neighbor_count = None

    def set_neighbors(self, neighbors):
        self.neighbor_count = len(self.neighbors)
        self.neighbors = neighbors
    
    def get_neighbors(self) -> list:
        if not None: return self.neighbors

    def set_draw_coords(self, WINDOW_WIDTH, WINDOW_HEIGHT) -> None:
        self.draw_x = (self.long + 180) * (WINDOW_WIDTH / 360)
        self.draw_y = ((self.lat * -1) + 90) * (WINDOW_HEIGHT / 180)

    def draw(self, WINDOW_WIDTH, WINDOW_HEIGHT) -> None:


        # only instantiates draw_x and draw_y when being drawn, might change
        self.draw_x = (self.long + 180) * (WINDOW_WIDTH / 360)
        self.draw_y = ((self.lat * -1) + 90) * (WINDOW_HEIGHT / 180)

        set_fill_color(0.9568, 0.9647, 0.1843) # yellow
        set_stroke_color(1, 0, 0)

        draw_circle(self.draw_x, self.draw_y, self.RADIUS)
    
    def in_circle(self, mouseX, mouseY):

        return sqrt((mouseX - self.draw_x)**2 + (mouseY - self.draw_y)**2) <= self.RADIUS

    def __str__(self) -> str:

        i = 0
        neigh_string = ""
        while i < len(self.neighbors) - 1:
            neigh_string += self.neighbors[i].iata + ","
            i += 1
        
        neigh_string += self.neighbors[i].iata

        return self.iata + "," + self.name + "," + self.city + ";" + neigh_string + "; " + str(self.lat) + "," + str(self.long)
