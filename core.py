import operator
import os
import redis
import json
import heapq
import sys


def open_fifo(path, fifos):
    if not os.path.exists(path):
        os.mkfifo(path)
    f = open(path, "w")
    fifos.append(f)
    return f


def hex_to_ip(h):
    o1 = int(h[0:1], 16)
    o2 = int(h[2:3], 16)
    o3 = int(h[4:5], 16)
    o4 = int(h[6:7], 16)
    return str(o1) + "." + str(o2) + "." + str(o3) + "." + str(o4)

def is_ipv4(ip_hex):
    """Checks if given IP is in IPv4 format
    Return type: Boolean"""
    return len(ip_hex)==8


def keys_with_max_vals(d, n):
    # The - is for python min-heap
    inverse = [[-p[1], p[0]] for p in d.items()]
    n = min(n, len(inverse))
    heapq.heapify(inverse)

    result = []
    for i in range(n):  # First n s
        elem = heapq.heappop(inverse)
        result.append([elem[1], -elem[0]])

    while len(inverse) > 0 and n > 0:  # The rest
        elem = heapq.heappop(inverse)
        if -elem[0] != result[n - 1][1]:
            break
        result.append([elem[1], -elem[0]])
    return result

def get_topk_with_skipped_count(count_dict, k):
    data = {}
    for outter_key in count_dict.keys():
        top_keys = keys_with_max_vals(count_dict[outter_key], k)
        for inner_key in count_dict[outter_key].keys():
            if inner_key in top_keys:
                data[outter_key][inner_key]=count_dict[outter_key][inner_key]
            else:
                if "skipped" not in data:
                    data[outter_key]["skipped"]=0
                    data[outter_key]["skipped_sum"]=0
                data[outter_key]["skipped"]+=1
                data[outter_key]["skipped_sum"]+=count_dict[outter_key][inner_key]
    return data

class RedisFile(object):

    def __init__(self, server, channel):
        self._r = redis.StrictRedis(host=server, db=0)
        self._channel = channel

    def write(self, value):
        self._r.publish(self._channel, value)

    def close(self):
        self._r.connection_pool.disconnect()


def mainloop(options):
    flist, window, input = options.prers, options.window_size, options.input
    counter = 0
    running = True
    while running:
        length = 0

        try:
            char = input.read(1)
            while char != '{':
                length = 10 * length + int(char)
                char = input.read(1)

            json_str = '{' + input.read(length - 1)
            json_dict = json.loads(json_str)
            packet = Packet(json_dict, window)
            counter += 1
            for fun in flist:
                try:
                    fun(packet)
                except PacketWithoutInfoError as pwie:
                    print >> sys.stderr, "The "+type(fun).__name__+" PreR"
                    print >> sys.stderr, "requires the \""+pwie.info+"\" info."
                    print >> sys.stderr, "Packet: "+str(packet)+"\n"

            if counter >= window:
                counter = 0
                for fun in flist:
                    f = fun.get_file()
                    message = {
                        "serverId": options.server_id,
                        "data": fun.get_data(),
                        "type": fun.get_type()
                    }
                    f.write(json.dumps(message))
                    f.write("\n")
                    fun.reset()
        except ValueError:
            running = False
            pass


# Counting-Sort
class PacketPocket(object):

    def __init__(self, k, n=1000):  # n es el tamano de la ventana en paquetes
        self._k = k
        self._reverse_dict = {}  # k define el top
        self._bucket_list = [set() for i in range(n + 1)]
        self._max_bucket = 1

    def incr_count(self, qname):
        if qname in self._reverse_dict:
            bucket = self._reverse_dict[qname]
            self._bucket_list[bucket + 1].add(qname)
            self._bucket_list[bucket].remove(qname)
            self._reverse_dict[qname] += 1
            if (bucket + 1 > self._max_bucket):
                self._max_bucket = bucket + 1
        else:
            self._reverse_dict[qname] = 1
            self._bucket_list[1].add(qname)

    def top_k(self):
        left = self._k
        ans = []
        next_bucket = self._max_bucket
        while (left > 0 and next_bucket > 0):
            keys = self._bucket_list[next_bucket]
            l = len(keys)
            if (l > 0):
                left -= l
                ans += keys
            next_bucket -= 1
        return ans


class PacketWithoutInfoError(Exception):
    """The Packet does not have the requested info.
    This usually happens because the serializer output does not have it.
    """

    def __init__(self, info):
        self._info = info

    def __str__(self):
        ans = "\n\tThis package does not have the '"
        ans += self._info
        ans += "' info.\n\tBe sure to set the serializer for including '"
        ans += self._info + "'"
        return ans

    @property
    def info(self):
        return self._info


class Packet(object):
    """Encapsulates the information packet and the size of its window
    """

    def __init__(self, input, window_size=1000):
        self._window_size = window_size
        self._input = input

    def __str__(self):
        return str(self._input)

    @property
    def input(self):
        """Return the input given to the packet"""
        return self._input

    @property
    def id(self):
        """Return the id of the packet"""
        try:
            return self._input['id']
        except KeyError:
            raise PacketWithoutInfoError('id')

    @property
    def qname(self):
        """Return the qname of the packet"""
        try:
            return self.query['qname'].lower()
        except KeyError:
            raise PacketWithoutInfoError('qname')

    @property
    def qtype(self):
        try:
            return self.query['qtype']
        except KeyError:
            raise PacketWithoutInfoError('qtype')

    @property
    def source(self):
        """Return the source of the packet"""
        try:
            return self._input['source']
        except KeyError:
            raise PacketWithoutInfoError('source')

    @property
    def dest(self):
        """Return the dest of the packet"""
        try:
            return self._input['dest']
        except KeyError:
            raise PacketWithoutInfoError('dest')

    @property
    def query(self):
        """Return some querie of the packet"""
        try:
            return self._input['queries'][0]
        except (KeyError, IndexError):
            raise PacketWithoutInfoError('queries')

    @property
    def window_size(self):
        """Return the window_size where is the packet"""
        return self._window_size


    def is_answer(self):
        """Return True if the packet is an answer"""
        try:
            flags = int(self._input['flags'], 16)
            return (flags & (1 << 15)) == (1 << 15)
        except KeyError:
            raise PacketWithoutInfoError('flags')

    def is_critical_type(self):
        """Return True if the packet type forbids
        have an underscore in its qname (for queries)"""
        try:
            return int(self.query['qtype'], 16) in [1, 2, 6, 15]
        except KeyError:
            raise PacketWithoutInfoError('qtype')


    ############# hedgehog stuff ##############
    @property
    def rd_bit(self):
        """Return the rd_bit of the packet
        Return type: Integer (1 or 0)"""
        pass

    @property
    def rcode(self):
        """Return the rcode of the packet
        Return type: Integer"""
        pass

    @property
    def opcode(self):
        """Return the opcode of the packet
        Return type: Integer"""
        pass

    @property
    def tc_bit(self):
        """Return the tc_bit of the packet
        Return type: Integer (1 or 0)"""
        pass

    @property
    def do_bit(self):
        """Return the do_bit of the packet
        Return type: Integer (1 or 0)"""
        pass

    @property
    def edns_version(self):
        """Returns the EDNS version of the packet
        Return type: Integer or None"""
        pass

    @property
    def transport_protocol(self):
        """Returns the transport protocol
        Return type: string"""
        pass

    @property
    def size(self):
        """Returns the packet size (in bytes)
        Return type: Integer"""
        pass

    def qclass(self):
        """Return the qclass of the packet
        Return type: Integer """
        pass

  @property
    def source_port(self):
        """Return the source port of the packet
        Return type: Integer """
        pass
