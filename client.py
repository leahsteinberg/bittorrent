import bencode, requests, hashlib, socket, struct
from bitstring import BitArray, BitStream
from messages import *
import time


message_ids = [choke, unchoke, interested, not_interested, have, bitfield, request, piece, cancel, port]


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
	for i in range(len(article['info']['files'])):
		left += article['info']['files'][i]['length']

# compact -> set to 1
# no_peer_id -> ignored if compact ==1
# event ->


parameters = {'info_hash': info_hash, 'peer_id': peer_id,
	'port': port, 'uploaded': 0, 'downloaded': 0, 'left': left, 'compact': 1, 'event': 'started'}

r = requests.get(url, params=parameters)
response = bencode.bdecode(r.content)
byte_r = response['peers']
byte_list = map(ord, byte_r)
int_list = byte_list[:]
peers = []

f = open("myfile.jpg", 'w')
i=0
while i < (len(int_list)):
  ip_addr = str(int_list[0+i]) + "."+str(int_list[1+i]) + "." + str(int_list[2+i]) + "." + str(int_list[3+i])
  peer_port = int_list[4+i]*256 +  int_list[5+i]
  peers.append(Peer(ip_addr, peer_port, f))
  i+=6
#print peers

for i in range(1, len(peers)):
  print i
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((peers[i].ip_addr, peers[i].port))
  pst = chr(19)
  reserved = chr(0)*8
  handshake = pst+'BitTorrent protocol'+reserved+info_hash+peer_id
  sock.send(handshake)
  recv_buff = sock.recv(100)
  print repr(recv_buff)
  if recv_buff[28:48] == info_hash:
    recv_buff = recv_buff[68:]
  while len(recv_buff)>0:
    recv_buff = parse(recv_buff, peers[i])
  recv_buff = sock.recv(100)
  print repr(recv_buff) + '/n'
  while len(recv_buff)>0:
    recv_buff = parse(recv_buff, peers[i])
  # send interested
  interested = "\x00\x00\x00\x01\x02"
  sock.send(interested)
  recv_buff = sock.recv(100)
  print repr(recv_buff)
  while len(recv_buff)>0:
    recv_buff = parse(recv_buff, peers[i])
  pieces_set = set(peers[i].pieces)
  
  print pieces_set
  for piece in pieces_set:
    hex_piece = chr(piece)
    request = "\x00\x00\x00\x0d\x06" + "\x00\x00\x00" + chr(piece) + '\x00\x00\x00\x00' + int_to_bytes(2**14)
    sock.send(request)
    time.sleep(.1)
    data = sock.recv(2**14+13)
    print str(piece) + "  got piece: " + str(len(data))
    parse(data, peers[i])
f.close()

