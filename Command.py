import io
import math
import copy
import socket
import struct
import threading
import multiprocessing
import time


class Command:
    def __init__(self):
        print("Entered Command")
        self.tcp_flag=True
        self.CMD_HEAD = "CMD_HEAD"
        self.CMD_MOVE = "CMD_MOVE"
        self.CMD_SONIC = "CMD_SONIC"
        self.HOST = '192.168.86.206'
        self.PORT = 5002
        self.client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket1.connect((self.HOST, self.PORT))
        self.receiveSonicDataThread=threading.Thread(target=self.receiveSonicData,args=(self.HOST,))
        self.latestSonicData = 0

    def receiveSonicData(self):
        while True:
            print("Entered receiveSonicData")
            alldata=self.receive_data()
            print(alldata)
            if alldata=='':
                break
            else:
                cmdArray=alldata.split('\n')
                print(cmdArray)
                if cmdArray[-1] !="":
                    cmdArray==cmdArray[:-1]
            for oneCmd in cmdArray:
                data=oneCmd.split("#")
                print(data)
                if data=="":
                    break
                elif data[0]==self.CMD_SONIC:
                    print('Obstacle:',data[1])
                    self.latestSonicData = int(data[1])
                    return data[1]

    def receive_data(self):
        print("Entered receive_data")
        data=""
        data=self.client_socket1.recv(1024).decode('utf-8')
        return data

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
        print("Entered Walking")
        try:
            command = self.CMD_MOVE + "1" +"0" + "35" + "0" + '\n'
            self.send_data(command)
            print(command)
        except Exception as e:
            print(e)
    def getSonicData(self):
        try:
            command = self.CMD_SONIC + '\n'
            self.send_data(command)
            print(command)
            time.sleep(.01)
            return self.latestSonicData
        except Exception as e:
            print(e)
