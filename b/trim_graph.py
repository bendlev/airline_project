# date: 04 nov 2022
# author: @bendlev
# purpose: eliminate all airports with no connections

f = open(r"temp\airports_destinations_bidir.txt", "r", encoding="utf-8")
o = open(r"temp\airports_trimmed.txt", "w", encoding="utf-8")

for l in f:
    iata, name, city = l.split(";")[0].split(",")
    neighbors = l.split(";")[1].split(",")
    lat, long = l.split(";")[2].split(",")
    if len(neighbors) > 0:

        i = 0
        neigh_str = ""
        while i < len(neighbors) - 1:
            neigh_str += neighbors[i] + ","
            i += 1

        neigh_str += neighbors[i]

        ostring = iata + "," + name + "," + city + ";" + neigh_str + ";" + lat + "," + long
        o.write(ostring)

f.close()
o.close()

