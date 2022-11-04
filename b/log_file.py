# date: 03 nov 2022
# author: @bendlev
# purpose: generate the log.txt showing status of each operation (read/write/merge)

import os
import datetime
import getpass

def main():
    os.chdir(".")

    username = getpass.getuser()
    usertime = datetime.datetime.now()

    print(f"{username} ran main.py on {usertime}.")

    f = open("log.txt", "w")

    f.write(f"Date generated: {usertime} \n")
    f.write(f"Username: {username} \n")
    f.write(f"Purpose: Proceeding with build of airport_graph.txt \n\n")

    f.write(f"====================\n\n")

    f.close()

main()


