from prer import PreR


class EdnsBufsiz(PreR):
    """Shows the count of the different rcodes for each reply in a window.

    - Result

    A dict that has an entry for each rcode captured where the key is the rcode
    (as an integer) and the value is the count of the packets having that rcode.

    - Example

    {
        0: 50, # No error
        1: 10, # Format error
        2: 1  # Server failure
    }


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """
    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._edns_bufsiz = {
            "0-511": 0,
            "512-1023": 0,
            "1024-1535": 0,
            "1536-2047": 0,
            "2048-2559": 0,
            "2600-3071": 0,
            "3072-3583": 0,
            "3584-4095": 0,
            "4096-4607": 0,
            "None": 0
        }

    def __call__(self, p):
        if not p.is_answer():
            if p.is_edns():
                ebs = p.edns_bufsiz
                if ebs >= 0 and ebs <= 511:
                    self._edns_bufsiz["0-511"] += 1
                elif ebs <= 1023:
                    self._edns_bufsiz["512-1023"] += 1
                elif ebs <= 1535:
                    self._edns_bufsiz["1024-1535"] += 1
                elif ebs <= 2047:
                    self._edns_bufsiz["1536-2047"] += 1
                elif ebs <= 2559:
                    self._edns_bufsiz["2048-2559"] += 1
                elif ebs <= 3071:
                    self._edns_bufsiz["2560-3071"] += 1
                elif ebs <= 3583:
                    self._edns_bufsiz["3072-3583"] += 1
                elif ebs <= 4095:
                    self._edns_bufsiz["3584-4095"] += 1
                elif ebs <= 4607:
                    self._edns_bufsiz["4096-4607"] += 1
            else:
                self._edns_bufsiz["None"] += 1


    def get_data(self):
        return self._edns_bufsiz


    def reset(self):
         self._edns_bufsiz = {
            "0-511": 0,
            "512-1023": 0,
            "1024-1535": 0,
            "1536-2047": 0,
            "2048-2559": 0,
            "2600-3071": 0,
            "3072-3583": 0,
            "3584-4095": 0,
            "4096-4607": 0,
            "None": 0
        }