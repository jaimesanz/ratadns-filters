from prer import PreR


class edns_versions(PreR):
    """Shows the count of the different edns_versions received for each query in
    a window.

    - Result

    A dict that has an entry for each edns_version captured where the key is an
    edns_version (as an integer) and the value is the count of the packets
    having that edns_version.

    - Example

    {
        None: 10, # without extensions
        0: 15 # Version 0
    }


    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._edns_versions = {}

    def __call__(self, p):
        if not p.is_answer():
            if p.is_edns():
                edns_version = p.edns_version
                if edns_version not in self._edns_versions:
                    self._edns_versions[edns_version]=0
                self._edns_versions[edns_version]+=1
            else:
                if "none" not in self._edns_versions:
                    self._edns_versions["none"]=0
                self._edns_versions["none"]+=1


    def get_data(self):
        return self._edns_versions


    def reset(self):
        self._edns_versions.clear()
