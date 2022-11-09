# Date: 09 March 2021.
# Author: Levesque, B.
# Purpose: Define a function to perform a breadth first search b/t start and goal vertices.

from collections import deque
from airport import Airport

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
    myset = set()

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

    print(f'This is conn: {conn}')
    print(f'I saw {count} attempts at paths, of which {count - conn} were unsuccessful.')
    
    print("These are the trouble-makers:\n")
    for a in err:
        print(a)

    return (sum / count), err # avg. len of all paths in graph , list of error airports

def full_average_breadth(airports: dict, limit = 10) -> list:

    avg_path_lens = []
    path_lens = []
    conn = 0
    err = []

    i = 0

    for k in airports.keys():
        sum = 0
        count = 0

        if i == limit:
            print(f'This is len of path_lens: {len(path_lens)}')
            print(f'This is len of avg_path_lens: {len(avg_path_lens)}')
            return path_lens, avg_path_lens # avg. len of all paths in graph


        for j in airports.keys():
            
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


    print(f'This is len of path_lens: {len(path_lens)}')
    print(f'This is len of avg_path_lens: {len(avg_path_lens)}')

    return path_lens, avg_path_lens # avg. len of all paths in graph