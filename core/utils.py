__author__ = 'franchoco'
import operator, os


def openfifo(path, fifos):
    if not os.path.exists(path):
        os.mkfifo(path)
    f = open(path, "w")
    fifos.append(f)
    return f


def hextoip(h):
   o1 = int(h[0:1], 16)
   o2 = int(h[2:3], 16)
   o3 = int(h[4:5], 16)
   o4 = int(h[6:7], 16)
   return str(o1) + "." + str(o2) + "." + str(o3) + "." + str(o4)


def keyswithmaxvals(d, n):
    sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    last_n = sorted_d[:n]
    return last_n