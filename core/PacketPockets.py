class PacketPocket1(object):
    def __init__(self, n,k): #n es el tamaño de la ventana en paquetes
        reverse_dict={}       #k define el top
        bucket_list=[{} for i in range(n)]
        max_bucket=1
        
    def incr_count(qname):
      if self.reverse_dict.has_key(qname):
          bucket = reverse_dict[qname]
          bucket_list[bucket + 1][qname] = True
          del(bucket_list[bucket][qname]])
          reverse_dict[qname] += 1
          if(bucket + 1 > max_bucket) 
            max_bucket = bucket + 1
      else:
          self.reverse_dict[qname]=1
          self.bucket_list[1][qname]=True

    def top-k():
      left=k
      ans=[]
      next_bucket=max_bucket
      while(left>0):
        keys=bucket_list[max_bucket].keys()
        l=len(keys)
        if(l>0):
          left-=l
          ans+=keys
        next_bucket-=1
      return ans
    def reset():
      reverse_dict={}
      bucket_list=[{} for i in range(n)]