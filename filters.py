#!/usr/bin/python2
import json, sys, time, operator, os

def main_loop(flist, window):
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

def keyswithmaxvals(d, n):
    sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    last_n = sorted_d[:n]
    return last_n

class FirstN(object):
    def __init__(self, f, n):
        self.f = f
        self.names = {}
        self.n = n

    def __call__(self, d):
        qname = d['queries'][0]['qname'].lower()

        if self.names.has_key(qname):
            self.names[qname] += 1
        else:
            self.names[qname] = 1

    def get_data(self):
        last_n = dict(keyswithmaxvals(self.names, self.n))
        return last_n

    def get_file(self):
        return self.f

    def reset(self):
        self.names.clear()

class NameCounter(object):
    def __init__(self, f):
        self.f = f
        self.names = {}

    def __call__(self, d):
        qname = d['queries'][0]['qname'].lower()
        if self.names.has_key(qname):
            self.names[qname] += 1
        else:
            self.names[qname] = 1

    def get_data(self):
        return self.names

    def get_file(self):
        return self.f

    def reset(self):
        self.names = {}

class PacketsPerSecond(object):
    def __init__(self, f):
        self.counter = 0
        self.start = time.time()
        self.f = f

    def __call__(self, d):
        self.counter += 1

    def get_data(self):
        data = { 'pps' : self.counter / (time.time() - self.start) }
        return data

    def get_file(self):
        return self.f

    def reset(self):
        self.counter = 0
        self.start = time.time()

class Identity(object):
    def __init__(self, f):
        self.f = f
        self.l = []
    def __call__(self, d):
        self.l.append(d)
    def get_data(self):
        return self.l
    def get_file(self):
        return self.f
    def reset(self):
        self.l = []

class PacketHasUnderscore(object):
    def __init__(self, f):
        self.f = f
        self.names = {}

    def __call__(self, d):
        qname = d['queries'][0]['qname']
        if "_" in qname:
            if self.names.has_key(qname):
                self.names[qname] += 1
            else:
                self.names[qname] = 1

    def get_data(self):
        return self.names

    def get_file(self):
        return self.f

    def reset(self):
        self.names.clear()



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
    #flist.append(FirstN(openfifo('first_20.fifo', fifos), 20))
    #flist.append(FirstN(sys.stdout, 20))
    #flist.append(PacketsPerSecond(openfifo('packets_per_second.fifo', fifos)))
    #flist.append(PacketsPerSecond(sys.stdout))
    #flist.append(PacketHasUnderscore(sys.stdout))
    #flist.append(PacketHasUnderscore(sys.stdout))
    #flist.append(Identity(sys.stdout))
    flist.append(NameCounter(sys.stdout))

    main_loop(flist, window)
