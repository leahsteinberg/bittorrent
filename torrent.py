class Torrent:
  def __init__(self, name):
    self.name = None 
    self.tracker_url = None 
    self.info_hash = None 
    self.length = None 
    self.piece_length = None 
    self.file_d = open(name, 'w') 
    
    

class Tracker:
  def __init__(self, peer_list):
    self.peers = peer_list


class Peer:  
  def choke(message):
    #print "choke"
    self.choked = True

  def unchoke(message):
    print "unchoke"
    self.choked = False
  
  def interested(message):
    pass

  def not_interested(message):
    pass

  def have(message):
    print "in have: "
    piece_have = ord(message[0])*(256**3)+ord(message[1])*(256**2)+ord(message[2])*(256**1)+ord(message[3])
    #passes in 4 byte payload -> representing one number.
    self.pieces.append(piece_have)
    print peer.pieces

  def request(message):
    pass

  def piece(message):
    # each four bytes... (same as request)
    # which piece we're talking about
    # where in the piece we are
    # 

    ## what I want to do here is:::
    # i have a message
    # i need to figure out what piece it is in
    # and find that piece object
    # then I want to make a temporary file
    # then I want to make a new block entry in the piece object
    # this block entry will be a tuple
    # the tuple will be (offset, temp_file)
    # i will get the offset from a place in the message

    #peer.piece[number]
    message = message[8:]
    self.file_d.write(message)
    self.file_d.flush()

  def cancel(message):
    pass

  def port(message):
    pass

  def bitfield(message):
    #print "in bitfield" + repr(message) + "\n"
    bit_field = ''
    for i in range(len(message)):
      bit_field += str(bin(ord(message[i]))[2:])
    #print bit_field
    for j in range(len(bit_field)):
      if bit_field[j]=='1':
        self.pieces.append(j)

  
  def __init__(self, ip_addr, peer_port):
    self.ip_addr = ip_addr
    self.socket = None
    self.port = peer_port
    self.pieces = []
    self.choked = True
    self.messages = []
    message_ids = [self.choke, self.unchoke, self.interested, self.not_interested, self.have, self.bitfield, self.request, self.piece, self.cancel, self.port]



  def parse(buff):
    print "start of parse"
    message_len = ord(buff[0])*(256**3)+ord(buff[1])*(256**2)+ord(buff[2])*(256**1)+ord(buff[3])
    message_type = ord(buff[4])
    # grab the message from the string based on the length
    message = buff[5:message_len+5]
    self.message_ids[message_type](message)
    buff = buff[message_len+4:]
    return buff

  def write_file():
    pass




class Piece:
  def __init__(self, number):
    self.number = number
    self.blocks = []
