# date: 08 nov 2022
# author: @bendlev
# purpose: sample visualization of two airports (and their path) in airport_graph.txt

from airport import Airport
from cs1lib import *
from breadth_first import breadth_first
from random import uniform


f = open(r"student/airport_graph.txt", "r", encoding="utf-8")

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
img = load_image(r"student/world_1800_900.jpg")

mouseX = 0
mouseY = 0

def myMouse(x, y):
    global mouseX, mouseY

    mouseX = x
    mouseY = y

# use to select unique airports

# def main():
#     global ndict, WINDOW_WIDTH, WINDOW_HEIGHT, mouseX, mouseY

#     clear()
#     draw_image(img, 0, 0)

#     for key in ndict:
#         set_fill_color(1, 0, 1)
#         ndict[key].draw(WINDOW_WIDTH, WINDOW_HEIGHT)

#     for key in ndict:
#         if ndict[key].in_circle(mouseX, mouseY):
#             set_fill_color(1, 1, 1)
#             draw_rectangle(0, 850, 200, 50)
#             set_font_size(16)
#             draw_text(key, 20, 885)

path1 = breadth_first(ndict["YTH"], ndict["FTU"])

print("===== Path 1 =====")
for p in path1:
    print(p.name)  
print("================") 

path2 = breadth_first(ndict["USH"], ndict["PYJ"])

print("===== Path 2 =====")
for p in path2:
    print(p.name)  
print("================") 

path3 = breadth_first(ndict["SCY"], ndict["SCT"])

print("===== Path 3 =====")
for p in path3:
    print(p.name)  
print("================") 

path4 = breadth_first(ndict["IVC"], ndict["EGS"])

print("===== Path 4 =====")
for p in path4:
    print(p.name)
print("================")   

path5 = breadth_first(ndict["SCC"], ndict["KCT"])

print("===== Path 5 =====")
for p in path5:
    print(p.name) 
print("================") 


for key in ndict:
    ndict[key].set_draw_coords(WINDOW_WIDTH, WINDOW_HEIGHT)

line_vals = []

# populate line_vals with x1, y1, x2, y2 for each line in the BFS path
def draw_paths(pathList):

    global line_vals

    r, g, b = 0.9568, 0.9647, 0.1843

    i = 0
    while i < len(pathList) - 1:

        line_vals.append([int(pathList[i].draw_x), int(pathList[i].draw_y), int(pathList[i+1].draw_x), int(pathList[i+1].draw_y), r, g, b])
        i += 1
    
    

# draw paths between points in a BFS path
# def main():
#     global ndict, WINDOW_WIDTH, WINDOW_HEIGHT, mouseX, mouseY

#     clear()
#     draw_image(img, 0, 0)

#     for key in ndict:
#         set_stroke_width(1)
#         set_fill_color(0, 1, 0)
#         ndict[key].draw(WINDOW_WIDTH, WINDOW_HEIGHT)

#     draw_paths(path5)

# start_graphics(main, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, mouse_move=myMouse)

def airportBot():
    print(f"== Welcome to Kommineni Air Ways! ==\n")
    print(f"We are focused on making your journey comfortable, and quick.\n")
    print(f"With our BFS search algorithm, we can find you the shortest path to your destination.\n\n")

    print(f"Here are our currently serviced airports:\n\n")
    i = 0

    airport_str = ""

    for key in ndict:
        # print airports 20 at a time, for each line
        if i % 20 == 0 and i != 0:
            airport_str += key + ", "  + "\n"
            i += 1
        else:
            airport_str += key + ", "
            i += 1

    print(airport_str + "\n")
    print(f"Where are you coming from? (Enter the 3-letter code which will serve as your Start vertex, and press [ENTER])\n")
    print(f"We suggest YTH -> FTU, USH -> PYJ, SCY -> SCT, IVC -> EGS, SCC -> KCT\n")
    startKey = input().upper()
    start = ndict[startKey]
    print(f"Great! You'll be starting from {startKey}: {ndict[startKey].name}\n\n")

    print(airport_str + "\n")
    print(f"Where are you going to? (Enter the 3-letter code which will serve as your Start vertex, and press [ENTER])\n")
    print(f"You'll be starting from {startKey}: {ndict[startKey].name}\n\n")
    print(f"We suggest YTH -> FTU, USH -> PYJ, SCY -> SCT, IVC -> EGS, SCC -> KCT\n")
    goalKey = input().upper()
    goal = ndict[goalKey]
    print(f"Great! You'll be starting from {goalKey}: {ndict[goalKey].name}\n\n")

    print(f"Departing from: {str(start)}\n")
    print(f"Arriving at: {str(goal)}\n\n")

    userPath = breadth_first(start, goal)

    pathStr = ""

    for i in range(len(userPath)):
        pathStr += userPath[i].name + "\n"

    print(f"To get there, it'll take {len(userPath)} stops. Including:\n")
    print(pathStr + "\n")

    print(f"== Thanks for Flying Kommineni Air Ways! ==")

    return userPath

# set start and goal vertices, get BFS path
myPath = airportBot()

# populate list_vals with 
draw_paths(myPath)

        

def main():

    global ndict, WINDOW_WIDTH, WINDOW_HEIGHT, mouseX, mouseY, myPath

    clear()
    draw_image(img, 0, 0)

    for key in ndict:
        set_stroke_width(1)
        set_fill_color(0, 1, 0)
        set_stroke_color(0, 1, 1)
        ndict[key].draw(WINDOW_WIDTH, WINDOW_HEIGHT)

    for line in line_vals:
        set_stroke_color(line[4], line[5], line[6])
        set_stroke_width(3)
        draw_line(line[0], line[1], line[2], line[3])


start_graphics(main, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, mouse_move=myMouse, title="Airport Pathfinder")