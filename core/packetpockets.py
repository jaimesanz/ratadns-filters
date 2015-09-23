#Counting-Sort
class PacketPocket1(object): 
    def __init__(self, n,k): #n es el tamaño de la ventana en paquetes
        self.reverse_dict = {}       #k define el top
        self.bucket_list = [{} for i in range(n)]
        self.max_bucket = 1
        
    def incr_count(self, qname):
      if self.reverse_dict.has_key(qname):
          bucket = self.reverse_dict[qname]
          self.bucket_list[bucket + 1][qname] = True
          del(self.bucket_list[bucket][qname]])
          self.reverse_dict[qname] += 1
          if(bucket + 1 > self.max_bucket) 
            self.max_bucket = bucket + 1
      else:
          self.reverse_dict[qname] = 1
          self.bucket_list[1][qname] = True

    def top_k(self):
      left = k
      ans = []
      next_bucket = self.max_bucket
      while(left > 0 && next_bucket > 0):
        keys = self.bucket_list[next_bucket].keys()
        l = len(keys)
        if(l > 0):
          left -= l
          ans += keys
        next_bucket -= 1
      return ans

#Maite-top-k
class PacketPocket2(object):
    def __init__(self, n,k): #n es el tamaño de la ventana en paquetes  #k define el top
       self.freq_dict = {}
       self.top_k_dict = {}
       self.min_val = 0
       self.mins = []
       self.tk_dict_size = 0

        
    def incr_count(qname):
      if (self.freq_dict.has_key(qname)):
        self.freq_dict[qname] += 1
      else:
        self.freq_dict[qname] = 1
      if (self.tk_dict_size < k):
        if (!self.top_k_dict.has_key[qname]):
          self.top_k_dict[qname] = True
          k -= 1
      else:
        if (self.freq_dict[qname] > min_val):
          a_min = self.mins.pop()
          del(self.top_k_dict[a_min])
          self.top_k_dict[qname] = True
          if (len(self.mins) == 0):
            self.extract_new_min(self.top_k_dict[qname])





    def top-k():
      
    def reset():
