# date: 08 nov 2022
# author: @bendlev
# purpose: sample visualization of two airports (and their path) in airport_graph.txt

from airport import Airport
from cs1lib import *


f = open("airport_graph.txt", "r", encoding="utf-8")

ndict = {}

## INSTANTIATE ALL AIRPORT OBJECTS ##

for l in f:
    iata, name, city = l.split(";")[0].split(",")
    neighbors = l.split(";")[1].split(",")
    lat, long = l.split(";")[2].split(",")

    ndict[iata] = Airport(iata, name, city, lat, long)
    ndict[iata].set_neighbors(neighbors)

f.close()

## REASSIGN ALL NEIGHBORS AS THEIR RESPECTIVE AIRPORT OBJECTS ##

for iata in ndict:

    nlist = []
    for neigh in ndict[iata].get_neighbors():
        if neigh != '' and neigh in ndict:
            neigh_obj = ndict[neigh] # the Airport object represented by the "neigh" iata (at present, all neighbors are IATA codes)
            nlist.append(neigh_obj)
    
    ndict[iata].set_neighbors(nlist)

WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 900
img = load_image("world_1800_900.jpg")

def main():

    draw_image(img, 0, 0)
    

start_graphics(main, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
