import logging
import socket
import pickle
import threading
import time
from typing import Optional
from API import Marker, Robot, Position
import struct
from logger import *
import random
import numpy as np

SERVER_ADDRESS = "robotpi-01.enst.fr"
SERVER_PORT = 65432

# A CHANGER
ROBOT_ID = 1

class Client:
    LOGGER_PREFIX = "co_"

    def __init__(self, id):
        self.logger: logging.Logger = setup_logger(
            Client.LOGGER_PREFIX+str(id))
        self.client_id: int = id
        self.socket: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.should_stop: bool = False
        self.answers: dict[type(Marker.Get) | type(Robot.Get), None] = {Marker.Get: None, Robot.Get: None}

        self.connect()

        self.recv_length: Optional[int] = None
        self.recv_thread = threading.Thread(
            target=Client.receive, args=(self,))
        self.recv_thread.start()

    def connect(self):
        self.socket.settimeout(1)
        self.socket.connect((SERVER_ADDRESS, SERVER_PORT))

    def receive(self):
        while not self.should_stop:
            try:
                raw_data: bytes = bytes()
                if self.recv_length is not None:
                    raw_data = self.socket.recv(self.recv_length)
                    if len(raw_data) <= 0:
                        self.logger.warning(
                            f"Server disconnected")
                        self.should_stop = True
                        break
                    self.recv_length = None
                else:
                    raw_data = self.socket.recv(4)
                    if len(raw_data) <= 0:
                        self.logger.warning(
                            f"Server disconnected")
                        self.should_stop = True
                        break
                    if len(raw_data) != 4:
                        self.logger.error(
                            f"Received a message of length {len(raw_data)}, but expected 4")
                        continue
                    self.recv_length = struct.unpack("i", raw_data)[0]
                    continue
                try:
                    data = pickle.loads(raw_data)
                except:
                    self.logger.error("Failed to decode data")
                    continue
                self.process_data(data)

            except ConnectionResetError:
                self.logger.error(
                    f"Connection deliberately closed by server")
                self.socket.close()
                self.should_stop = True
                break

            except socket.timeout as timeout_exception:
                continue

    def handshake(self):
        self.socket.send(struct.pack("i", self.client_id))

    def process_data(self, data):
        self.logger.info(f"Received {data} from server")
        if isinstance(data, Marker.GetAnswer):
            self.answers[Marker.Get] = data
        elif isinstance(data, Robot.GetAnswer):
            self.answers[Robot.Get] = data
        

    def send(self, obj):
        message: bytes = pickle.dumps(obj)
        self.socket.sendall(struct.pack("i", len(message)))
        self.socket.sendall(message)
    
    def request_sync(self, obj):
        self.send(obj)
        while self.answers[obj.__class__] == None:
            continue
        answer = self.answers[obj.__class__]
        self.answers[obj.__class__] = None
        return answer

    def send_bytes(self, data: bytes):
        self.socket.sendall(struct.pack("i", len(data)))
        self.socket.sendall(data)

    def stop(self):
        self.should_stop = True
        self.recv_thread.join()

# EXEMPLE D'UTILISATION
if __name__ == "__main__":
    setup_loggers()
    ROBOT_ID = int(sys.argv[1])
    client = Client(ROBOT_ID)
    try:
        logging.info("Starting client...")
        # The first message sends the robot's id
        client.handshake()
        client.send(Marker.Post(1, Position(float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))))
        answer: Marker.GetAnswer = client.request_sync(Marker.Get(1))
        logging.debug(f"Parsed response is id: {answer.robot_id} position: {answer.position}")

    except KeyboardInterrupt as e:
        logging.warning("Catched CTRL-C")
    except Exception as e:
        logging.error("Catched exception")
        logging.error(f"{e}")

    client.stop()
