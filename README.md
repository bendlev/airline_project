# airport_graph_project
Repository for the development of the [COSC1](https://dartmouth.smartcatalogiq.com/current/orc/Departments-Programs-Undergraduate/Computer-Science/COSC-Computer-Science-Undergraduate/COSC-1) Lab 4 assignment to be deployed at Dartmouth College in Winter 2023. All files are original work, unless specified otherwise.

***

This repo contains all of the files necessary to generate `airport_graph.txt`. The universe of this file is all airports in the world, based on the most recent [data](https://github.com/jpatokal/openflights/tree/master/data) from the [OpenFlights](https://openflights.org/data) project (data until 2014).

The `\raw` folder contains `airports.dat` and `routes.dat`, OpenFlights files that are pulled in the build file. These are held in case the OpenFlights GitHub is deprecated.

Dependencies:

`pandas` package (`python3.x -m pip install pandas`)
`numpy` package

Note:

This was developed on a Windows machine, file paths that work on that system may not work on other devices.
