class Torrent:
  def __init__(self, name):
    self.name = None 
    self.tracker_url = None 
    self.info_hash = None 
    self.length = None 
    self.piece_length = None 
    self.file_d = open(name, 'w+')
    self.received = 0

class Tracker:
  def __init__(self, peer_list):
    self.peers = peer_list


class Peer:  
  def choke(self, message):
    self.choked = True

  def unchoke(self, message):
    print "unchoked"
    self.choked = False
  
  def interested(self, message):
    pass

  def not_interested(self, message):
    pass

  def have(self, message):
    print "in have: "
    piece_have = ord(message[0])*(256**3)+ord(message[1])*(256**2)+ord(message[2])*(256**1)+ord(message[3])
    #passes in 4 byte payload -> representing one number.
    self.pieces.append(piece_have)
    print "has piece: " + str(piece_have)

  def request(self, message):
    pass

  def piece(self, message):
    #print "in piece" 
    ## what I want to do here is:::
    # i have a message
    # i need to figure out what piece it is in
    # and find that piece object
    # then I want to make a temporary file
    # then I want to make a new block entry in the piece object
    # this block entry will be a tuple
    # the tuple will be (offset, temp_file)
    # i will get the offset from a place in the message
    # p_index is which piece this is
    if len(message) < 8:
      print "short message, len is : " + str(len(message))
      return
    p_index = ord(message[0])*(256**3)+ord(message[1])*(256**2)+ord(message[2])*(256**1)+ord(message[3])
    # p_begin is the offset into this piece
    p_begin = ord(message[4])*(256**3)+ord(message[5])*(256**2)+ord(message[6])*(256**1)+ord(message[7])

    print "in piece, with piece #: " + str(p_index)
    message = message[8:]
    # if this peer...?? doesnt have any other pieces??
    #if len(self.data) == 0:
    # make a new piece with this index
    
    if p_index in self.piece_recv:
      for i in range(len(self.data)):
        # go find this piece in the peer's array of pieces
        if self.data[i].number == p_index:
          # grab the piece that this block belongs to.
          this_piece = self.data[i]
          break
    else:
      this_piece = Piece(p_index)
      self.data.append(this_piece)
      self.piece_recv.append(p_index)
    # now that you have the piece
    # go into the piece's file to the place we need to start,
    # and write the message to this piece's file.
    this_piece.file_d.seek(p_begin)
    print "in piece, len mesage" + str(len(message))
    this_piece.file_d.write(message)
    


  def cancel(self, message):
    pass

  def port(self, message):
    pass

  def bitfield(self, message):
    print "in bitfield"
    bit_field = ''
    for i in range(len(message)):
      bit_field += str(bin(ord(message[i]))[2:])
    #print bit_field
    for j in range(len(bit_field)):
      if bit_field[j]=='1':
        self.pieces.append(j)
        print "in bf, has: " + str(j)

  
  def __init__(self, ip_addr, peer_port):
    self.ip_addr = ip_addr
    self.socket = None
    self.port = peer_port
    self.pieces = []
    self.choked = True
    self.messages = []
    self.message_ids = [self.choke, self.unchoke, self.interested, self.not_interested, self.have, self.bitfield, self.request, self.piece, self.cancel, self.port]
    self.data = []
    self.piece_recv = []


  def parse(self, buff):
    if len(buff)< 5:
      print "in parse, length of buffer too small"
      return
    message_len = ord(buff[0])*(256**3)+ord(buff[1])*(256**2)+ord(buff[2])*(256**1)+ord(buff[3])
    message_type = ord(buff[4])
    print "in parse, message type: " + str(message_type)
    # grab the message from the string based on the length
    message = buff[5:message_len+5]
    self.message_ids[message_type](message)
    buff = buff[message_len+4:]
    return buff

  def write_file(self):
    pass




class Piece:
  def __init__(self, number):
    # should make the file the lenght of the piece..fill it up with zeros
    self.number = number
    self.string = 'temp' + str(number) + '.jpg'
    self.file_d = open(self.string, 'w+')
