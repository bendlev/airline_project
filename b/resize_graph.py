# date: 04 nov 2022
# author: @bendlev
# purpose: read airports_trimmed.txt, generate dictionary, discover the size and see what's missing

import operator
import numpy as np
# from a.breadth_first import average_breadth

f = open(r"temp\airports_trimmed.txt", "r", encoding="utf-8")

rstring = "Airport data will be collected in an Airport object and used to construct graph.\n"
rstring += "resize_graph.py will check the size of the largest tree in the graph,\n and eliminate airports outside of largest tree.\n"

ndict = {}

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
    
    def __str__(self) -> str:

        i = 0
        neigh_string = ""
        while i < len(self.neighbors) - 1:
            neigh_string += self.neighbors[i].iata + ","
            i += 1
        
        neigh_string += self.neighbors[i].iata

        return self.iata + "," + self.name + "," + self.city + ";" + neigh_string + "; " + str(self.lat) + "," + str(self.long)


## BFS FUNCTIONS ##

from collections import deque

def breadth_first(start, goal):


    frontier = deque()
    frontier.append(start)
    
    backpointer = {}
    backpointer[start] = None

    while len(frontier) > 0:

        v = frontier.popleft()

        if v == goal:
            # If we're done, retrace the path from goal to start
            path = []
            while v != None:
                path.append(v)
                v = backpointer[v]
            return path
        else: # keep exploring
            for neighbor in v.get_neighbors():

                if not neighbor in backpointer:

                    backpointer[neighbor] = v
                    frontier.append(neighbor)

    return None

def average_breadth(airports: dict, start: Airport) -> int:

    # only need to start with a single airport in order to find paths
    # should be n-1 paths from start to all vertices in graph

    # if not true, then the graph is several trees
    
    count = 0
    sum = 0
    conn = 0
    err = []

    # while 

    for j in airports.keys():
        path = breadth_first(start, airports[j])
        if path != None:
            sum += len(path)
            conn += 1
        if path == None:
            # print(f'Between ({start.name}) and ({airports[j].name}), a path exists.')
            err.append(airports[j])
        count += 1

    # print(f'This is conn: {conn}')
    # print(f'I saw {count} attempts at paths, of which {count - conn} were unsuccessful.')
    
    # print("These are the trouble-makers:\n")
    # for a in err:
    #     print(a)

    return (sum / count), err # avg. len of all paths in graph , list of error airports

def full_average_breadth(airports: dict, limit = 30) -> list:

    avg_path_lens = []
    path_lens = []
    conn = 0
    err = []

    i = 0

    for k in airports:
        sum = 0
        count = 0

        if i == limit:
            # print(f'This is len of path_lens: {len(path_lens)}')
            # print(f'This is len of avg_path_lens: {len(avg_path_lens)}')
            return path_lens, avg_path_lens # avg. len of all paths in graph


        for j in airports:
            
            path = breadth_first(airports[k], airports[j])
            if path != None:
                path_lens.append(len(path)) 
                sum += len(path)
                conn += 1
            if path == None:
                # print(f'Between ({start.name}) and ({airports[j].name}), a path exists.')
                err.append([airports[k], airports[j]])
            count += 1

        avg_path_lens.append([float(sum / count), airports[k].name])

        i += 1
        print(f"{i}: Ding!")


    # print(f'This is len of path_lens: {len(path_lens)}')
    # print(f'This is len of avg_path_lens: {len(avg_path_lens)}')

    return path_lens, avg_path_lens # avg. len of all paths in graph




## FILE READS ##

for l in f:
    iata, name, city = l.split(";")[0].split(",")
    neighbors = l.split(";")[1].split(",")
    lat, long = l.split(";")[2].split(",")

    ndict[iata] = Airport(iata, name, city, lat, long)
    ndict[iata].set_neighbors(neighbors)

f.close()

for iata in ndict:

    nlist = []
    for neigh in ndict[iata].get_neighbors():
        if neigh != '' and neigh in ndict:
            neigh_obj = ndict[neigh] # the Airport object represented by the "neigh" iata (at present, all neighbors are IATA codes)
            nlist.append(neigh_obj)
    
    ndict[iata].set_neighbors(nlist)


# alist = []
# for key in ndict:
#     alist.append(ndict[key])

# alist.sort(key=operator.attrgetter("neighbor_count"), reverse=False)

most_connected = "AMS" # using above sort, ATL was the most connected

avg_breadth, errs = average_breadth(ndict, ndict[most_connected])

rstring += f"Using {ndict[most_connected].name} as the starting point, the size of the BFS graph was {len(ndict) - len(errs)}.\n"
rstring += f"{len(errs)} 'lonely airports' will be deleted from the forest, resulting in a single connected tree of {len(ndict) - len(errs)} nodes.\n\n"

for a in errs:
    # print(a.iata)
    del ndict[a.iata]

f = open("a/airport_graph.txt", "w", encoding="utf-8")

for key in ndict:
    iata = ndict[key].iata
    name = ndict[key].name
    city = ndict[key].city
    lat = ndict[key].lat
    long = ndict[key].long
    neighbors = ndict[key].get_neighbors()

    nlist = []

    # delete duplicates left behind in neighbors list

    # print(f"This is the length of neighbors: {len(neighbors)}")
    for n in neighbors:
        if n not in nlist:
            nlist.append(n)

    i = 0
    neigh_string = ""
    while i < len(nlist) - 1:
        neigh_string += nlist[i].iata + ","
        i += 1
    
    neigh_string += nlist[i].iata


    # print(f"This is the length of nlist: {len(nlist)}")


    ostring = iata + "," + name + "," + city + ";" + neigh_string + ";" + lat + "," + long
    f.write(ostring)

f.close()

## REREAD AFTER DROPPING EXTRA NEIGHBORS ##

f = open(r"a/airport_graph.txt", "r", encoding="utf-8")

for l in f:
    iata, name, city = l.split(";")[0].split(",")
    neighbors = l.split(";")[1].split(",")
    lat, long = l.split(";")[2].split(",")

    ndict[iata] = Airport(iata, name, city, lat, long)
    ndict[iata].set_neighbors(neighbors)

f.close()

for iata in ndict:

    nlist = []
    for neigh in ndict[iata].get_neighbors():
        if neigh != '' and neigh in ndict:
            neigh_obj = ndict[neigh] # the Airport object represented by the "neigh" iata (at present, all neighbors are IATA codes)
            nlist.append(neigh_obj)
    
    ndict[iata].set_neighbors(nlist)

alist = []
for key in ndict:
    alist.append(ndict[key])


# for a in alist:
    # print(str(a) + ", " + str(len(a.get_neighbors())))
rstring += f"====================\n\n"

rstring += f"airport_graph.txt has been generated with {len(ndict)} Airports, each connected with bi-directional edges.\n"
rstring += f"Given the patchwork nature of the available data (airports.dat and routes.dat),\nthe previous operations were neccesary "
rstring += f"in to generate a clean dataset to suit course needs.\n\n"

rstring += f"Basic Graph Analysis:\n\n"

alist.sort(key=operator.attrgetter("neighbor_count"), reverse=True)

rstring += f"The most connected airport is {alist[0].name}.\n"

alist.sort(key=operator.attrgetter("neighbor_count"), reverse=False)

rstring += f"The least connected airport is {alist[0].name}.\n\n"

rstring += f"Uncomment lines 284-292 in resize_graph.py to run BFS analysis. Runtime is ~2.6 sec/node."

# pathlens, avg_path_lens = full_average_breadth(ndict, limit=30)

# sum = 0
# for a in avg_path_lens:
#     sum += a[0]

# avg_of_avg = sum / len(avg_path_lens)

# rstring += f"Treating {len(avg_path_lens)} nodes as Start, finding a BFS to all other nodes, the average BFS path length was {round(avg_of_avg, 4)}.\n"
