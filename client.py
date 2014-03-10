import bencode, requests, hashlib, socket, struct
from bitstring import BitArray, BitStream



class Peer():
  def __init__(self, ip_addr, port):
    self.ip_addr = ip_addr
    self.port = port


article = bencode.bdecode(open('demo.torrent', 'rb').read())
# url encoded -> ??? figure out
url = article['announce']

# PARAMETERS

# info_hash -> value of "info"
		# get NON decoded info dictionary, then hash it. (????)
info = article['info']
info_hash = hashlib.sha1(bencode.bencode(info)).digest()
# peer_id -> no guidelines
peer_id = '-LS0001-123456781235' # 20 bytes
# port
port = 6881
# uploaded -> total amnt uploaded

# downloaded ->

# left
### need to check if one or multiple files..
if article['info'].get('length'):
	left = article['info']['length']
else:
	left = 0
	for i in range(len(article['info']['files'][i]['length'])):
		left += article['info']['files'][i]['length']

# compact -> set to 1
# no_peer_id -> ignored if compact ==1
# event ->
event = 'started'


parameters = {'info_hash': info_hash, 'peer_id': peer_id,
	'port': port, 'uploaded': 0, 'downloaded': 0, 'left': left, 'compact': 1, 'event': event}

r = requests.get(url, params=parameters)
response = bencode.bdecode(r.content)
byte_r = response['peers']
byte_list = map(ord, byte_r)
int_list = byte_list[:]

peers = []

i=0
while i < (len(int_list)):
  ip_addr = str(int_list[0+i]) + "."+str(int_list[1+i]) + "." + str(int_list[2+i]) + "." + str(int_list[3+i])
  peer_port = int_list[4+i]*256 +  int_list[5+i]
  peers.append(Peer(ip_addr, peer_port))
  i+=6

for i in range(len(peers)):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  print "peers i ipaddr" + peers[i].ip_addr
  sock.connect(peers[i].ip_addr)
  pst = chr(19)
  reserved = chr(0)*8
  handshake = pst+'BitTorrent protocol'+reserved+info_hash+peer_id
  sock.send(handshake)
  recv_buff = sock.recv(100)
  if len(recv_buff) == 68:
    if recv_buff[28:48] == info_hash:
      print "this is a handshake!!"
      recv_buff = recv_buff[68:]
      print "should have deleted the handshake from the buffer"
      print recv_buff


def choke(message):
  pass

def unchoke(message):
  pass

def interested(message):
  pass

def not_interested(message):
  pass

def have(message):
  print "in have"

def request(message):
  pass

def piece(message):
  pass

def cancel(message):
  pass

def port(message):
  pass

def bitfield(message):
  print "in bitfield"






message_ids = [choke, unchoke, interested, not_interested, have, bitfield, request, piece, cancel, port]

recv_buff = sock.recv(100)

def parse(buff):
  #print "start of parse"
  #print repr(buff)
  message_len = ord(buff[0])*(256**3)+ord(buff[1])*(256**2)+ord(buff[2])*(256**1)+ord(buff[3])
  id = ord(buff[4])
  # grab the message from the string based on the length
  message = buff[:message_len+5]
  message_ids[id](message)
  buff = buff[message_len+4:]
  print "end of parse"
  print repr(buff)
  return buff



while len(recv_buff)>0:
  recv_buff = parse(recv_buff)


