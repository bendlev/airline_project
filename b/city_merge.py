# date: 03 nov 2022
# author: @bendlev
# purpose: artificial merge

# given the nature of aiports_destinations.csv, it is difficult to handle in a
# Dataframe or similar structure. This file opens city_names.csv (the list of all city names in world_cities.txt)

# if city_name[i] is in a dict formed by airports_destinations.csv, it stays. else, drop

f = open("temp/city_names.csv", "r")

city_names = []
rstring = ""

for l in f:
    city_names.append(l)

f.close()

# temp\airports_destinations_bidir.txt
f = open("temp/airports_destinations_bidir.txt", "r", encoding="utf-8")
m = open("working/airports_cities_merged.txt", "w", encoding="utf-8")

for l in f:
    # GKA,Goroka Airport,Goroka;HGU,LAE,MAG,POM,POM;-6.08169,145.391998
    city = l.split(";")[0].split(",")[2]
