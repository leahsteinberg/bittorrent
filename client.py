import bencode, requests, hashlib, socket, struct
import errno
from bitstring import BitArray, BitStream
from messages import *
from torrent import *
import time
import select

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
  parameters = {'info_hash': torr.info_hash, 'peer_id': torr.peer_id,
	'port': port, 'uploaded': 0, 'downloaded': 0, 'left': torr.length, 'compact': 1, 'event': 'started'}

  return parameters

def get_peers(url, parameters):
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
## ISSUE ... HOW DOES THIS GET INFO OF INFO HASH AND PEER ID!!!!!!!!
def handshake(peer, torr):
  peer.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  peer.socket.setblocking(0)
  peer.socket.settimeout(5)
  try:
    peer.socket.connect((peer.ip_addr, peer.port))
  except socket.error, e:
    return False
  pst = chr(19)
  reserved = chr(0)*8
  handshake = pst+'BitTorrent protocol'+reserved+torr.info_hash+torr.peer_id
  peer.socket.send(handshake)
  try:
    recv_buff = peer.socket.recv(100)
  except peer.socket.error, e:
    return False
  if recv_buff[28:48] == torr.info_hash:
    recv_buff = recv_buff[68:]
  else:
    return False
  while len(recv_buff)>0:
    recv_buff = tracker.peers[i].parse(recv_buff)
    print "parsing buffer, got stuff after handshake "
  return True


def send_interested(peer):
    interested = "\x00\x00\x00\x01\x02"
    peer.socket.send(interested)
    time.sleep(.1)
    recv_buff = peer.socket.recv(100)
    print repr(recv_buff)
    while len(recv_buff)>0:
      recv_buff = peer.parse(recv_buff)


def request_pieces(torrent, peer):
    print "in request_pieces"
    for piece in set(peer.pieces):
      request = "\x00\x00\x00\x0d\x06" + "\x00\x00\x00" + chr(piece) + '\x00\x00\x00\x00' + int_to_bytes(2**14)
      peer.socket.send(request)
      time.sleep(2)
      if torrent.length - torrent.received > 2**14:
        data = peer.socket.recv(2**14+13)
      else:
        data = peer.socket.recv((torrent.length - torrent.received)+13)
      torrent.received+= len(data)
      print "data len: " + str(len(data))
      peer.parse(data)

def write_data(torr, tracker):
  for i in range(len(tracker.peers)):
    print tracker.peers[i].data
    for j in range(len(tracker.peers[i].data)):
      tracker.peers[i].data[j].file_d.seek(0)
      temp_buff = tracker.peers[i].data[j].file_d.read(torr.piece_length)
      print str(j) + "     " + str(len(temp_buff))
      torr.file_d.seek(tracker.peers[i].data[j].number*torr.piece_length) 
      torr.file_d.write(temp_buff)
      torr.file_d.flush()



def main_func():
  article = bencode.bdecode(open('demo.torrent', 'rb').read())
  torr = Torrent(article['info']['name'])
  parameters = open_torrent(torr, article)
  tracker = Tracker(get_peers(torr.tracker_url, parameters))
  bad_peers = []
  for i in range(len(tracker.peers)):
    hs = handshake(tracker.peers[i], torr)
    if hs:
      send_interested(tracker.peers[i])
    else:
        bad_peers.append(i)
        print "removed peer" +  str(i)
  for i in range(len(tracker.peers)):
      if i not in bad_peers:
        if tracker.peers[i].choked == False:
          request_pieces(torr, tracker.peers[i])
  write_data(torr, tracker)


if __name__ == '__main__':
    main_func()




