import time, base64, hmac, hashlib, json
from urllib.parse import quote
from websocket import create_connection  # pip install websocket-client

API_KEY = '<입력하세요>'
SECRET = '<입력하세요>'

timestamp = str(int(time.time() * 1000))
msg = 't' + timestamp
key = base64.b64decode(SECRET)
signature = base64.b64encode(
  hmac.new(key, str(msg).encode('utf-8'), hashlib.sha512).digest()
).decode()

url = 'wss://wsapi.gopax.co.kr?apiKey={}&timestamp={}&signature={}'
url = url.format(quote(API_KEY), timestamp, quote(signature))
ws_conn = create_connection(url, timeout=10)
ws_conn.settimeout(None)

request = {
  'i': 1,  # 생략해도 무방
  'n': 'SubscribeToOrderBook',
  'o': {'tradingPairName': 'BCH-KRW'}
}
ws_conn.send(json.dumps(request))

while True:
  raw_response = ws_conn.recv()
  if raw_response.startswith('"primus::ping::'):  # 큰따옴표 유념 요망
    ws_conn.send('"primus::pong::' + raw_response[15:])
  else:
    response = json.loads(raw_response)
    print(json.dumps(response, indent=2))