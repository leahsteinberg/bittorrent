import bencode, requests, hashlib, socket, struct
from bitstring import BitArray, BitStream
from messages import *
from torrent import *
import time

def main_func():
  article = bencode.bdecode(open('demo.torrent', 'rb').read())
  torr = Torrent(article['info']['name'])
  parameters = open_torrent(torr, article)
  tracker = Tracker(get_peers(parameters))
  for peer in tracker.peers:
    if handshake(peer): 
      send_request(peer)

def open_torrent(torr, article):
  torr.tracker_url = article['announce']
  info = article['info']
  torr.info_hash = hashlib.sha1(bencode.bencode(info)).digest()
  torr.peer_id = '-LS0001-123456781235'
  port = 6881
  if article['info'].get('length'):
          torr.length =  article['info']['length']
          torr.piece_length = article['info']['piece length']
          # what is going on here?? need to capture length and piece_length here
  else:
	  torr.length = 0
          torr.piece_length = article['info']['files'][0]['piece length']
	  for i in range(len(article['info']['files'])):
	  	torr.length += article['info']['files'][i]['length']
               
  parameters = {'info_hash': info_hash, 'peer_id': peer_id,
	'port': port, 'uploaded': 0, 'downloaded': 0, 'left': torr.length, 'compact': 1, 'event': 'started'}
  return parameters

def get_peers(parameters):
  r = requests.get(url, params=parameters)
  response = bencode.bdecode(r.content)
  byte_r = response['peers']
  byte_list = map(ord, byte_r)
  int_list = byte_list[:]
  i=0
  peer_list = []
  while i < (len(int_list)):
    ip_addr = str(int_list[0+i]) + "."+str(int_list[1+i]) + "." + str(int_list[2+i]) + "." + str(int_list[3+i])
    peer_port = int_list[4+i]*256 +  int_list[5+i]
    peer_list.append(Peer(ip_addr, peer_port))
    i+=6
  return peer_list


## if the handshake works, this should clear out the received buffer once it returns. (is this true??)
def handshake(peer):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((tracker.peers[i].ip_addr, tracker.peers[i].port))
  pst = chr(19)
  reserved = chr(0)*8
  handshake = pst+'BitTorrent protocol'+reserved+torr.info_hash+torr.peer_id
  sock.send(handshake)
  recv_buff = sock.recv(100)
  if recv_buff[28:48] == torr.info_hash:
    recv_buff = recv_buff[68:]
  else:
    return False
  while len(recv_buff)>0:
    recv_buff = peer.parse(recv_buff, peers[i])
  return True


def get_messages():
    recv_buff = sock.recv(100)
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

