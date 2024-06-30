import os
import multiprocessing as mp
import jwt  # PyJWT
import uuid
import websocket  # websocket-client
import pyupbit
from dotenv import load_dotenv

load_dotenv()

access_key = os.environ['ACCESS_KEY']
secret_key = os.environ['SECRET_KEY']

queue = mp.Queue()
proc = mp.Process(
    target=pyupbit.WebSocketClient,
    args=('ticker', ["KRW-BTC"], queue),
    daemon=True
)