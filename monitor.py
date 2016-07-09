import fileinput, subprocess

str = "[W 160708 11:51:21 iostream:651] error on read: [Errno 113] No route to host"

if __name__ == "__main__":

    for line in fileinput.input():
        print line
        if "error on read" in line:
            print "Server connection is dead"
            
