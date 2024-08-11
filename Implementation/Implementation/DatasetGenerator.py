from os import stat
import pandas as pd
import CANInterface
import UDSFunctions


class DatasetGenerator:
    def __init__(self):
        self.__can = CANInterface.CANInterface(interface=CANInterface.CAN_INTERFACE, channel=CANInterface.CAN_CHANNEL, 
                bitrate=CANInterface.CAN_BITRATE, state=CANInterface.CAN_STATE)
        
        self.__uds_functions = UDSFunctions.DiagFunctions()

    def can_dataset(self):
        available_uds_sessions = [0x1, 0x3, 0x40, 0x4F, 0x60]
        for session in available_uds_sessions:
            i = 0
            can_data = {
                'Timestamp':        [],
                'Arbitration_ID':   [],
                'Ext_Identifier':   [],
                'Data_Length_Code': [],
                'Payload':          []
            }    
            self.__uds_functions.setsession(session=session)
            while i < 5000:
                can_message = self.__can.receive()
                can_data['Timestamp'].append(can_message.timestamp)
                can_data['Arbitration_ID'].append(can_message.arbitration_id)
                can_data['Ext_Identifier'].append(can_message.is_extended_id)
                can_data['Data_Length_Code'].append(can_message.dlc)
                can_data['Payload'].append((bytes(can_message.data)))

                i = i + 1

            can_dataset = pd.DataFrame(data=can_data)
            can_dataset.to_csv('UDS_Session_' + str(session) + '.csv')

dataset_generator = DatasetGenerator()
dataset_generator.can_dataset()