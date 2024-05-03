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
            #self.__feature_extractor = FeatureExtractorCollection()
            #self.__database_client = DatabaseClient.DatabaseClient(db_host=DatabaseClient.DB_HOST, db_port=DatabaseClient.DB_PORT)
            
        def receive(self):
            id_freq = 0.0
            id_msg = 0
            data_len = 0

            recv_msg = self.__can_interface.receive()
            #transition_aggregation_vector = [0] * (recv_msg.dlc * 8)
            print(recv_msg)

            row_data = [recv_msg.arbitration_id, recv_msg.timestamp, recv_msg.data]  # Assuming relevant attributes
            with open(csv_file_path, mode='a', newline='') as file:  # Mode 'a' for append
                writer = csv.writer(file)
                writer.writerow(row_data)
                print("Data exported to CSV successfully!")

            #if self.__id_list.check_id(recv_msg.arbitration_id):
            #    feature_list = self.__feature_extractor.get_features(can_msg=self.__id_list.get_can_node_by_id(recv_msg.arbitration_id), 
             #       campaign='FeatureCampaign')
              #  id_freq = feature_list[0]
               # id_msg = feature_list[1]
                #data_len = feature_list[2]
                #transition_aggregation_vector = feature_list[3]

            #self.__id_list.insert_element(id=recv_msg.arbitration_id, curr_occ=recv_msg.timestamp, freq_time=id_freq, freq_msg=0, 
             #       curr_msg=recv_msg)
            #self.__database_client.insert_data(timestamp=recv_msg.timestamp, id=recv_msg.arbitration_id, msg_freq_time=id_freq, 
             #       msg_freq=id_msg, data_len=data_len, tav=transition_aggregation_vector)

print("DEBUG: Entry")
can_recorder = CANRecoder()
print("DEBUG: Init Class")
print("DEBUG: Entering While True..")
while True:
   can_recorder.receive()