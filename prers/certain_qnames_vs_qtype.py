from core import keys_with_max_vals
from prer import PreR


class certain_qnames_vs_qtype(PreR):
    """For each qtype it shows the count of the top 200 TLDs of the queries
    received.

    - Result

    A dict having a key for each qtype whose value is another dict which has an
    entrie for each top 200 TLD where the key is the TLD and the value is the
    count. It also includes the key 'skipped' with the number of skipped
    TLDs and the key 'skipped_sum' with the sum of the counts of each skipped
    TLD.

    - Example

    {
        #qtypes are integers
        1: { # For illustration purposes we will just work with the top 2 TLDs
             # in this example
            'cl': 100,
            'com': 40,
            'skipped': 40,
            'skipped_sum': 400
        },
        2: {
            'net': 69
        }
    }

    - Complexity Note

    <FILL>

    - ReductionRatio Note

    <FILL>
    TODO review this docstring
    """

    def __init__(self, f, **kwargs):
        PreR.__init__(self, f)
        self._certain_qnames_vs_qtype = {}

    def __call__(self, p):
      #   <CertainQnames val="localhost">
    		# <Qtype count="8814" val="1"/>
      #   	<Qtype count="85010" val="28"/>
      #   </CertainQnames>

      #   <CertainQnames val="X.rootservers.net">
      #   	<Qtype count="85010" val="1"/>
      #   	<Qtype count="9215" val="28"/>
      #   </CertainQnames>

      #   <CertainQnames val="else">
      # 		<Qtype count="92852" val="1"/>
      #   	<Qtype count="31442" val="12"/>
      #   	<Qtype count="9215" val="28"/>
      #   </CertainQnames>

      qname = p.qname
      qtype = p.qtype

      if qname == "localhost.":
      	self.incr_count("localhost", qtype)
      elif qname.endswith("root-servers.net."):
      	self.incr_count("root-servers.net", qtype)
      else:
      	self.incr_count("else", qtype)

    def get_data(self):
    	return self._certain_qnames_vs_qtype

    def reset(self):
        self._certain_qnames_vs_qtype.clear()

   	def incr_count(self, qname, qtype):
		if qname not in self._certain_qnames_vs_qtype:
  			self._certain_qnames_vs_qtype[qname]={}
  		if qtype not in self._certain_qnames_vs_qtype[qname]:
  			self._certain_qnames_vs_qtype[qname][qtype]=0
  		self._certain_qnames_vs_qtype[qname][qtype]+=1