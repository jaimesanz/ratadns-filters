__author__ = 'franchoco'
import operator, os, heapq


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
    inverse = [[-p[1], p[0]] for p in d.items()] #The - is for min-heap python :)
    n = min(n, len(inverse))
    heapq.heapify(inverse)

    result = []
    for i in range(n): #First n s
        elem = heapq.heappop(inverse)
        result.append([elem[1], -elem[0]])

    while len(inverse) > 0 and n>0: #The rest
        elem = heapq.heappop(inverse)
        if -elem[0] != result[n-1][1]:
            break
        result.append([elem[1], -elem[0]])
    return result



class PacketsPocket(object):
    def __init__(self, n,k): #n es el tamano de la ventana en paquetes
        reverse_dict={}       #k define el top
        bucket_list=[{} for i in range(n)]

    def incr_count(qname):
      if self.reverse_dict.has_key(qname):
          bucket=reverse_dict[qname]
          bucket_list[bucket+1][qname]=True
          del(bucket_list[bucket][qname])
          reverse_dict[qname]+=1
          if(bucket + 1 > max_bucket):
              max_bucket = bucket + 1
      else:
          self.reverse_dict[qname]=1
          self.bucket_list[1][qname]=True

    def reset():
      reverse_dict={}
      bucket_list=[{} for i in range(n)]




