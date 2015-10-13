__author__ = 'franchoco'
import sys, json

def mainloop(flist, window, input):
    counter = 0
    running = True
    while running:
        length = 0

        try:
            char = input.read(1)
            while char != '{':
                length = 10*length + int(char)
                char = input.read(1)

            json_str = '{' + input.read(length-1)
            json_dict = json.loads(json_str)
            counter += 1
            for fun in flist:
                fun(json_dict)
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

