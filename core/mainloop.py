__author__ = 'franchoco'
import sys, json
from packet import Packet

def mainloop(flist, window):
    counter = 0
    running = True
    while running:
        length = 0

        try:
            char = sys.stdin.read(1)
            while char != '{':
                length = 10*length + int(char)
                char = sys.stdin.read(1)

            json_str = '{' + sys.stdin.read(length-1)
            json_dict = json.loads(json_str)
            packet = Packet(json_dict, window)

            counter += 1
            for fun in flist:
                fun(packet)
            if counter >= window:
                counter = 0
                for fun in flist:
                    f = fun.get_file()
                    json.dump(fun.get_data(), f)
                    f.write("\n")
                    fun.reset()
        except ValueError:
            running = False
            pass

