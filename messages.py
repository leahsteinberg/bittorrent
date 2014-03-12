from bitstring import BitArray, BitStream

class Peer():
  def __init__(self, ip_addr, port, myfile):
    self.ip_addr = ip_addr
    self.port = port
    self.pieces = []
    self.choked = True
    self.f = myfile

def choke(message, peer):
  #print "choke"
  peer.choked = True

def unchoke(message, peer):
  #print "unchoke"
  peer.choked = False
  

def interested(message, peer):
  pass

def not_interested(message, peer):
  pass

def have(message, peer):
  #print "in have: "
  piece_have = ord(message[0])*(256**3)+ord(message[1])*(256**2)+ord(message[2])*(256**1)+ord(message[3])
  #passes in 4 byte payload -> representing one number.
  peer.pieces.append(piece_have)
  #print peer.pieces

def request(message, peer):
  pass

def piece(message, peer):
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

def cancel(message, peer):
  pass

def port(message, peer):
  pass

def bitfield(message, peer):
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


message_ids = [choke, unchoke, interested, not_interested, have, bitfield, request, piece, cancel, port]



def int_to_bytes(number):
  #TO DO... CASE OF **3 AND **4 ARE BADDDDDDDD
  if number < 256:
    result = '\x00\x00\x00' + chr(number)
  elif number < 256**2:
    result = '\x00\x00' + chr(number/256) + chr(number%256)
  elif number< 256**3:
    number2 = number/(256**2)
    number3 = number2/256
    result = '\x00' + chr(number2) + chr(number3) + chr(number%256)
  elif number < 256**4:
    number1 = number/(256**3)
    number2 = number1/(256**2)
    number3 = number2/256
    result = chr(number1) + chr(number2) + chr(number3) + chr(number%256)

  else:
    # Throw overflow exception
    print "Overflow exception"
    result = None
  return result


