# date: 08 nov 2022
# author: @bendlev
# purpose: Airport class, used for visualization

# students will have to code this themselves to suit airport_graph.txt

from cs1lib import *

class Airport:

    def __init__(self, iata, name, city, lat, long) -> None:
        self.iata = iata
        self.name = name
        self.city = city
        self.lat = lat
        self.long = long

        self.neighbors = []
        self.neighbor_count = None

    def set_neighbors(self, neighbors):
        self.neighbor_count = len(self.neighbors)
        self.neighbors = neighbors
    
    def get_neighbors(self) -> list:
        if not None: return self.neighbors

    def draw(self, WINDOW_WIDTH, WINDOW_HEIGHT) -> None:

        RAD = 5

        draw_x = (self.long + 180) * (WINDOW_WIDTH / 360)
        draw_y = ((self.lat * -1) + 90) * (WINDOW_HEIGHT / 180)

        draw_circle(draw_x, draw_y, RAD)
    
    def __str__(self) -> str:

        i = 0
        neigh_string = ""
        while i < len(self.neighbors) - 1:
            neigh_string += self.neighbors[i].iata + ","
            i += 1
        
        neigh_string += self.neighbors[i].iata

        return self.iata + "," + self.name + "," + self.city + ";" + neigh_string + "; " + str(self.lat) + "," + str(self.long)
