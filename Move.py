import io
import math
import copy
import socket
import struct
import threading
import multiprocessing
import time

class Move:
    def __init__(self):
        print("Entered Move")
        self.tcp_flag=True
        self.CMD_HEAD = "CMD_HEAD"
        self.CMD_MOVE = "CMD_MOVE"
        self.HOST = '192.168.86.206'
        self.PORT = 5002
        self.client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket1.connect((self.HOST, self.PORT))
    def send_data(self,data):
        if self.tcp_flag:
            try:
                self.client_socket1.send(data.encode('utf-8'))
                print("Sent")
            except Exception as e:
                print(e)
    def headUpAndDown(self,angle):
        try:
            command = self.CMD_HEAD + "#" +"0" +"#"+str(angle) + '\n'
            self.send_data(command)
            print(command)
        except Exception as e:
            print(e)
    def headLeftAndRight(self,angle):
        try:
            command = self.CMD_HEAD + "#" +"1" +"#"+str(angle) + '\n'
            self.send_data(command)
            print(command)
        except Exception as e:
            print(e)
    def walk(self):
        try:
            command = self.CMD_MOVE + "1" +"0" + "35" + "0" + '\n'
            self.send_data(command)
            print(command)
        except Exception as e:
            print(e)
