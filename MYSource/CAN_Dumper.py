import can
import os
import csv

from CAN_List import CANList

CAN_INTERFACE = 'socketcan'
CAN_CHANNEL = 'can0'
CAN_STATE = can.bus.BusState.PASSIVE
CAN_BITRATE = 500000
csv_file_path = "dump.csv"

class CAN_Interface:
    def __init__(self, interface, channel, bitrate, state):
        self.__interface = interface
        self.__channel = channel
        self.__bitrate = bitrate
        self.__state = state

        if interface == 'socketcan':
            self.__start_socketCAN()

        self.__config_can()
        self.__can_bus = can.Bus()

    def __start_socketCAN(self):
        os.system('sudo modprobe peak_usb')
        os.system('sudo ip link set ' + self.__channel + ' down')
        os.system('sudo ip link set up ' + self.__channel + ' type can bitrate ' + str(self.__bitrate))    
    
    def __config_can(self):
        can.rc['interface'] = self.__interface
        can.rc['channel'] = self.__channel
        can.rc['state'] = self.__state
        can.rc['bitrate'] = self.__bitrate

    def receive(self):
        recv_message = self.__can_bus.recv()
        return recv_message

class CANRecoder():
        def __init__(self):
            print("DEBUG: Init CAN Interface..")
            self.__can_interface = CAN_Interface(interface=CAN_INTERFACE, channel=CAN_CHANNEL, 
                bitrate=CAN_BITRATE, state=CAN_STATE)
            self.__id_list = CANList()
 
        def receive(self):
            id_freq = 0.0
            id_msg = 0
            data_len = 0

            recv_msg = self.__can_interface.receive()
            print(recv_msg)

            row_data = [recv_msg.arbitration_id, recv_msg.timestamp, recv_msg.data]  # Assuming relevant attributes
            with open(csv_file_path, mode='a', newline='') as file:  # Mode 'a' for append
                writer = csv.writer(file)
                writer.writerow(row_data)
                print("Data exported to CSV successfully!")

print("DEBUG: Entry")
can_recorder = CANRecoder()
print("DEBUG: Init Class")
print("DEBUG: Entering While True..")
while True:
   can_recorder.receive()