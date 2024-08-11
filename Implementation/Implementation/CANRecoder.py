import CANInterface
from FeatureExtractorCollection import FeatureExtractorCollection
from CANList import CANList
import DatabaseClient


class CANRecoder():
        def __init__(self):
            self.__can_interface = CANInterface.CANInterface(interface=CANInterface.CAN_INTERFACE, channel=CANInterface.CAN_CHANNEL, 
                bitrate=CANInterface.CAN_BITRATE, state=CANInterface.CAN_STATE)
            self.__id_list = CANList()
            self.__feature_extractor = FeatureExtractorCollection()
            self.__database_client = DatabaseClient.DatabaseClient(db_host=DatabaseClient.DB_HOST, db_port=DatabaseClient.DB_PORT)
            
        def receive(self):
            id_freq = 0.0
            id_msg = 0
            data_len = 0

            recv_msg = self.__can_interface.receive()
            transition_aggregation_vector = [0] * (recv_msg.dlc * 8)
            print(recv_msg)
            if self.__id_list.check_id(recv_msg.arbitration_id):
                feature_list = self.__feature_extractor.get_features(can_msg=self.__id_list.get_can_node_by_id(recv_msg.arbitration_id), 
                    campaign='FeatureCampaign')
                id_freq = feature_list[0]
                id_msg = feature_list[1]
                data_len = feature_list[2]
                #transition_aggregation_vector = feature_list[3]

            self.__id_list.insert_element(id=recv_msg.arbitration_id, curr_occ=recv_msg.timestamp, freq_time=id_freq, freq_msg=0, 
                    curr_msg=recv_msg)
            self.__database_client.insert_data(timestamp=recv_msg.timestamp, id=recv_msg.arbitration_id, msg_freq_time=id_freq, 
                    msg_freq=id_msg, data_len=data_len, tav=transition_aggregation_vector)


can_recorder = CANRecoder()
while True:
   can_recorder.receive()