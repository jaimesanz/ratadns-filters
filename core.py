__author__ = 'franchoco'

import operator, os, redis, json

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

#deprecated
def keyswithmaxvals(d, n):
    sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    last_n = sorted_d[:n]
    return last_n

class RedisFile(object):
    def __init__(self, server, channel):
        self.r = redis.StrictRedis(host=server, db=0)
        self.channel = channel

    def write(self, value):
        self.r.publish(self.channel, value)

    def close(self):
        self.r.connection_pool.disconnect()

def mainloop(options):
    flist, window, input = options.prers, options.window_size, options.input
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
                    s = json.dumps(fun.get_data())
                    f.write(s + "\n")
                    fun.reset()
        except ValueError:
            running = False
            pass

#Counting-Sort
class PacketPocket(object):
    def __init__(self, k, n): #n es el tamano de la ventana en paquetes
        self.k = k
        self.reverse_dict = {}       #k define el top
        self.bucket_list = [set() for i in range(n+1)]
        self.max_bucket = 1

    def incr_count(self, qname):
        if self.reverse_dict.has_key(qname):
            bucket = self.reverse_dict[qname]
            self.bucket_list[bucket + 1].add(qname)
            self.bucket_list[bucket].remove(qname)
            self.reverse_dict[qname] += 1
            if(bucket + 1 > self.max_bucket):
                self.max_bucket = bucket + 1
        else:
            self.reverse_dict[qname] = 1
            self.bucket_list[1].add(qname)

    def top_k(self):
        left = self.k
        ans = []
        next_bucket = self.max_bucket
        while(left > 0 and next_bucket > 0):
            keys = self.bucket_list[next_bucket]
            l = len(keys)
            if(l > 0):
                left -= l
                ans += keys
            next_bucket -= 1
        return ans