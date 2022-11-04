# date: 03 nov 2022
# author: @bendlev
# purpose: prepare world_cities.txt as a .csv, to be merged onto airports_destinations.csv (deprecated)

f = open("raw/world_cities.txt", "r")
out = open("temp/city_names.csv", "w")

# out.write("city_name\n")

for line in f:
    line = line.split(",")
    city_name = line[1]
    out.write(city_name + "\n")

f.close()
out.close()
