#!/usr/bin/python2
import json, sys, time, operator, os

def main_loop(flist, window):
    counter = 0
    while True:
        length = 0

        char = sys.stdin.read(1)
        while char != '{':
            length = 10*length + int(char)
            char = sys.stdin.read(1)
        
        json_str = '{' + sys.stdin.read(length-1)
        json_dict = json.loads(json_str)
        counter += 1
        for f in flist:
            f(json_dict)
        if counter >= window:
            counter = 0
            for f in flist:
                f.send_data()
                f.reset()
        

def keyswithmaxvals(d, n):
    sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    last_n = sorted_d[:n]
    return last_n

class First20(object):
    def __init__(self, f):
        self.f = f
        self.names = {}
        self.counter = 0

    def __call__(self, d):
        qname = d['queries'][0]['qname']

        if self.names.has_key(qname):
            self.names[qname] += 1
        else:
            self.names[qname] = 1

        self.counter +=1 

    def send_data(self):
        last_n = keyswithmaxvals(self.names, 20)
        for name, count in last_n:
            self.f.write(name + ":" + str(count) + "\n")
        self.f.write("\n\n")

    def reset(self):
        self.names = {}
        self.counter = 0

class PacketsPerSecond(object):
    def __init__(self, f):
        self.counter = 0
        self.start = time.time()
        self.f = f

    def __call__(self, d):
        self.counter += 1

    def send_data(self):
        pps = self.counter / (time.time() - self.start)
        self.f.write("Avg packets/sec: " + str(pps) + "\n\n")

    def reset(self):
        self.counter = 0
        self.start = time.time()

def openfifo(path, fifos):
    if not os.path.exists(path):
        os.mkfifo(path)
    f = open(path, "w")
    fifos.append(f)
    return f

if __name__ == '__main__':
    window = 1000

    fifos = [] # To close files

    flist = []
    flist.append(First20(openfifo('first_20.fifo', fifos)))
    flist.append(PacketsPerSecond(openfifo('packets_per_second.fifo', fifos)))

    main_loop(flist, window)
