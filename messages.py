from bitstring import BitArray, BitStream

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


