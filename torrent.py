class Torrent:
  def __init__(self, name):
    self.name = None #
    self.tracker_url = None #
    self.info_hash = None #
    self.length = None #
    self.piece_length = None #
    self.file_d = open(name, 'w') #
    
    

class Tracker:
  def __init__(self, peer_list):
    self.peers = peer_list


class Peer:
  def __init__(ip_addr, peer_port):
    self.ip_addr = ip_addr
    self.port = port
    self.pieces = []
    self.choked = True
    self.messages = []
    message_ids = [choke, unchoke, interested, not_interested, have, bitfield, request, piece, cancel, port]


  
  def choke(message):
    #print "choke"
    peer.choked = True

  def unchoke(message):
    #print "unchoke"
    peer.choked = False
  

  def interested(message):
    pass

  def not_interested(message):
    pass

  def have(message):
    #print "in have: "
    piece_have = ord(message[0])*(256**3)+ord(message[1])*(256**2)+ord(message[2])*(256**1)+ord(message[3])
    #passes in 4 byte payload -> representing one number.
    peer.pieces.append(piece_have)
    #print peer.pieces

  def request(message):
    pass

  def piece(message):
    # each four bytes... (same as request)
    # which piece we're talking about
    # where in the piece we are
    # length of piece
    # here is where I want to write to file object
    ## also get rid of other stuff
    #file.write message from 12 on
    message = message[8:]
    peer.f.write(message)
    peer.f.flush()

  def cancel(message):
    pass

  def port(message):
    pass

  def bitfield(message):
    #print "in bitfield" + repr(message) + "\n"
    bit_field = ''
    #print len(message)
    #print repr(message)
    for i in range(len(message)):  ## deal w endian issue
      #print "i in bit: " + str(i)
      bit_field += str(bin(ord(message[i]))[2:])
    #print bit_field
    for j in range(len(bit_field)):
      if bit_field[j]=='1':
        peer.pieces.append(j)
    #print "end of bitfield: "
    #print peer.pieces
    

  def parse(buff, peer):
    #print "start of parse"
    message_len = ord(buff[0])*(256**3)+ord(buff[1])*(256**2)+ord(buff[2])*(256**1)+ord(buff[3])
    id = ord(buff[4])
    # grab the message from the string based on the length
    message = buff[5:message_len+5]
    #print "in parse: " + repr(message)
    message_ids[id](message, peer)
    buff = buff[message_len+4:]
    return buff




class Piece:
  def __init__():
    pass
