import can
import os
import csv
import threading
import time
import sys 
  
from CAN_List import CANList

CAN_INTERFACES = ['socketcan', 'socketcan', 'socketcan','socketcan', 'socketcan', 'socketcan']  # List of interfaces for each channel
CAN_CHANNELS = ['can0', 'can1', 'can2', 'can3', 'can4', 'can5']  # List of channels
CAN_STATES = [can.bus.BusState.PASSIVE, can.bus.BusState.PASSIVE, can.bus.BusState.PASSIVE, can.bus.BusState.PASSIVE, can.bus.BusState.PASSIVE, can.bus.BusState.PASSIVE]  # List of states for each channel
CAN_BITRATE = 500000

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

class CANRecoder(threading.Thread):
    def __init__(self, interface, channel, state):
        threading.Thread.__init__(self)
        self.__can_interface = CAN_Interface(interface=interface, channel=channel, bitrate=CAN_BITRATE, state=state)
        self.__id_list = CANList()
        self.csv_file_path = f"{channel}_dump.csv"
        self.running = True
        print(interface)
 
    def run(self):
        start_time = time.time()
        while self.running:
            recv_msg = self.__can_interface.receive()
            print(recv_msg)
            data_str = ' '.join([format(byte, '02X') for byte in recv_msg.data])
            row_data = [recv_msg.arbitration_id, recv_msg.timestamp, data_str]  # Assuming relevant attributes
            with open(self.csv_file_path, mode='a', newline='') as file:  # Mode 'a' for append
                writer = csv.writer(file)
                writer.writerow(row_data)
                #print(f"Data exported to {self.csv_file_path} successfully!")
            if time.time() - start_time >= timeinterval:
                self.running = False
                print("Recording stopped after 10 seconds.")

print("DEBUG: Entry")
print("This is the name of the program:", sys.argv[0]) 
print("Argument List:", str(sys.argv)) 
timeinterval = int(sys.argv[1])

# Create and start threads for each CAN channel
threads = []
for i in range(len(CAN_CHANNELS)):
    thread = CANRecoder(interface=CAN_INTERFACES[i], channel=CAN_CHANNELS[i], state=CAN_STATES[i])
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
