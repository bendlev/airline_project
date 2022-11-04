# date: 03 nov 2022
# author: @bendlev
# purpose: pull openflights data from github, write to .csv for later merge

import requests
import os

url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"
r = requests.get(url)

# s = requests.get(r"https://raw.githubusercontent.com/jpatokal/openflights/tree/master/data/routes.dat")
rstring = ""
alist = []

def airports_data():

    global alist, rstring

    # input:
    # id, name, city, country, IATA, ICAO, latitude, longitude, altitude, timezone, DST, TZ database time zone, type, source (data)

    # function writes to .csv:
    # id, name, city, country, IATA, latitude, longitude

    data = r.content
    data = data.splitlines()

    mini_str = f"Opened airlines.dat, and found {len(data)} airports."
    rstring += mini_str + "\n"

    f = open("./temp/airports.csv", "w", encoding="utf-8") # encoding "utf-8" prevents bad char-mapping

    count = 0

    for da in data:
        
        new = str(da, encoding="utf-8") # must cast to str to split(","), must use encoding here (again)
        # print(new)
        new = new.split(",")
        
        new[0] = new[0].lstrip("b'")

        nlist = [int(new[0])]

        # clean name, city, country, IATA
        for i in range(1, 5, 1):
            new[i] = new[i].lstrip("'")
            new[i] = new[i].rstrip("'")
            new[i] = new[i].lstrip('"')
            new[i] = new[i].rstrip('"')
            nlist.append(new[i])
        
        # attempt to cast latitude and longitude to proper types, otherwise pass
        try:
            new[6] = round(float(new[6]), 6)
        except:
            pass

        try:
            new[7] = round(float(new[7]), 6)
        except:
            pass

        nlist.append(new[6])
        nlist.append(new[7])

        # id [0], name [1], city [2], country [3], IATA [4], latitude [6], longitude [7]

        
        if str(new[4]) == r'\N': # skip observations with missing data
            continue
        else:
            count += 1
            i = 0
            nstring = ""
            while i < len(nlist) - 1:
                nstring += str(nlist[i]) + ","
                i += 1
            nstring += str(nlist[i])
            f.write(nstring + "\n")

            # print(new[4])
            alist.append(new[4]) # if full data exists for the airport, record it (used for eliminating erroneous routes later)

    rstring += f"Generated airlines.csv, with {count} valid observations out of {len(data)} observations in the dataset.\n"
    rstring += f"Though {len(data)} observations were identified, {count} had all information required to record them. A drop in {len(data) - count} observations.\n"
    rstring += f"It should be noted that the id numbers in airports.dat read up to 14000, while the real number of airports is {len(data)} in the data.\n\n"
    f.close()

    # return rstring
    
airports_data()


url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat"
s = requests.get(url)

ndict = {}

def routes_data():
    global ndict, rstring

    # input:
    # airline, airline ID, source airport (IATA or ICAO), source airport ID (openflights-specific),
    # destination airport (IATA or ICAO), destination airport id (openflights-specific), codeshare, stops,
    # equipment

    # function writes to .csv:
    # source airport, destination airport

    data = s.content
    data = data.splitlines()

    rstring += f"Opened routes.dat, and found {len(data)} routes.\n"
    out = open("temp/routes.csv", "w")

    for da in data:
        
        new = str(da, encoding="utf-8") # must cast to str to split(","), must use encoding here (again)
        # print(new)
        new = new.split(",")
        
        new[0] = new[0].lstrip("b'")

        source = new[2]
        dest = new[4]

        out.write(source + "," + dest + "\n")

        if source not in ndict:
            ndict[source] = []

        ndict[source].append(dest)

    out.close()

routes_data()

# print(ndict)

f = open("./temp/airports.csv", "r", encoding="utf-8")
n = open("./temp/airports_destinations.txt", "w", encoding="utf-8")

# print(alist)
# print(len(alist))

def clean_routes_data():

    global rstring

    rstring += "Ensuring that all destination airports are found in airports.csv. If not, they will be omitted as valid destinations.\n"

    airport_count = 0
    valid_dest_count = 0
    invalid_dest_count = 0

    for line in f:

        line = line.strip()
        line = line.split(",")

        iata = line[4]
        name = line[1]
        city = line[2]
        country = line[3]
        latitude = line[5]
        longitude = line[6]

        if iata in ndict:
            neighbors = ndict[iata]
            airport_count += 1
            # print(neighbors)
        else: # skip over iata not included in ndict, maybe not perfect but keys like 'HFN' having trouble
            continue

        neigh_str = ""

        # only add neighbors if the neighbors themselves have full data avaiable
        for nei in neighbors:
            if nei in alist:
                valid_dest_count += 1
                neigh_str += nei + ","
            else:
                invalid_dest_count += 1

        # print(neigh_str)
        nstring = iata + "," + name + "," + city + ";" + neigh_str.rstrip(",") + ";" + latitude + "," + longitude
        # print(nstring)
        n.write(nstring + "\n")

    perc = (valid_dest_count) / (valid_dest_count + invalid_dest_count)
    perc = round(perc, 4)

    rstring += f"Out of {airport_count} airports previously identified, there were {valid_dest_count} valid destinations out of {valid_dest_count + invalid_dest_count} total recorded destinations. {perc}% of destinations were valid.\n"
    rstring += f"While {len(alist)} airports had characteristic data, {len(ndict)} had available route data. A drop in {len(alist) - len(ndict)} observations.\n\n"

    n.close()

clean_routes_data()

one = open("temp/airports_destinations.txt", "r", encoding="utf-8")

rstring += f"Now ensuring that all source-destination connections are bi-directional in the graph.\n"

ndict = {}

for line in one:
    line = line.split(";")
    info = line[0].split(",")
    iata = info[0]
    neighbors = line[1].split(",")
    ndict[iata] = neighbors

    # print(f"{iata} has these neighbors: {neighbors}")

one.close()


neighbor_count = 0
repairs = 0

for key in ndict: # for each IATA in ndict

    # grab the neighbors for that IATA
    neighbors = ndict[key]

    # for each neighbor
    for neigh in neighbors:
        neighbor_count += 1
        # if the IATA is not also in the list of neigh's neighbors (ndict[neigh]), append to ndict[neigh] with that IATA
        # TODO: Check below if-statement for inherent (bad) assumptions
        if neigh != '' and neigh in ndict and key not in ndict[neigh]: # if neigh is an actual IATA code, then check 
            repairs += 1
            ndict[neigh].append(key)

rstring += f"Of the {neighbor_count} total neighbors among all airports, {repairs} ({round(repairs / neighbor_count,4)}%) were not bi-directional.\n"

two = open("temp/airports_destinations.txt", "r", encoding="utf-8")
three = open("temp/airports_destinations_bidir.txt", "w", encoding="utf-8")

rstring += f"All source-destination connections are now bi-directional in the graph. Rewriting onto airports_destinations_bidir.txt file.\n"

# ndict = {}

for line in two:
    line = line.split(";")
    info, city, name = line[0].split(",") # iata, name
    iata = info
    neighbors = ndict[iata] # cleaned/repaired neighbors
    lat, long = line[2].split(",") # lat, long

    i = 0
    neigh_string = ""
    while i < len(ndict[iata]) - 1:
        neigh_string += ndict[iata][i] + ","
        i += 1
    
    neigh_string += ndict[iata][i]

    wstring = iata + "," + city + "," + name + ";" + neigh_string + ";" + lat + "," + long
    three.write(wstring)

    # print(f"{iata} has these neighbors: {neighbors}")

two.close()
three.close()