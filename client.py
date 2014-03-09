import bencode, requests, hashlib


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
response['peers']


first four numbers = ip
next two = pport --
port
num1, num2
(num1*256)+num2=
# need to convert the peers value into bytes
# will be an array of number.. first 4 are ip address, second 2 are port...

print peers

# ip -> optional, numwant -> optional, key -> optional

