# date: 03 nov 2022
# author: @bendlev
# purpose: generate Lab 4 data from scratch

import b.log_file as log

import b.prepare_openflights_data
# import b.trim_graph doesn't do anything in practice, accounted for somewhere earlier?
import b.resize_graph

log.main()



f = open("log.txt", "a")

text = b.prepare_openflights_data.rstring
f.write(text + "\n")

text = b.resize_graph.rstring
f.write(text + "\n")

f.close()