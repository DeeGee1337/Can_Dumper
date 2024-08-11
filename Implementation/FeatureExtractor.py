from abc import ABC, abstractmethod
import sys
from datetime import datetime
from bitstring import BitArray


class FeatureExtractor(ABC):
    @abstractmethod
    def extract_features(self, can_msg):
        pass


class FeatureExtractorIDFrequency(FeatureExtractor):
    def extract_features(self, can_msg):
        last_datetime = datetime.utcfromtimestamp(can_msg.get_last_occ())
        curr_datetime = datetime.utcfromtimestamp(can_msg.get_curr_occ())

        id_frequency = self.__calc_frequency(last_occur=last_datetime, curr_occur=curr_datetime)

        return id_frequency

    def __calc_frequency(self, last_occur, curr_occur):
        if (curr_occur <= last_occur):
            print('ERROR', "Last occurence can't be bigger then current occurence", file=sys.stderr)
            exit()
        else:   
            period = (curr_occur - last_occur).total_seconds()
            freq = 1.0 / period

        return freq


class FeatureExtractorIDMsgFrequency(FeatureExtractor):
    def extract_features(self, can_msg):
        msg_in_between = can_msg.get_freq_msg()
        can_msg.reset_freq_msg()
        return msg_in_between

class FeatureExtractorDataLength(FeatureExtractor):
    def extract_features(self, can_msg):
        data_len = can_msg.get_curr_msg().dlc
        return data_len

class FeatureExtractorTAV(FeatureExtractor):
    def extract_features(self, can_msg):
        payload_len_curr = can_msg.get_curr_msg().dlc * 8

        if can_msg.get_last_msg() is not None:
            payload_len_last = can_msg.get_last_msg().dlc * 8
        else:
            payload_len_last = payload_len_curr

        transition_aggregation_vector = [0] * payload_len_curr

        if can_msg.get_last_msg() is not None:
            last_payload_bitarray = BitArray(bytes=bytes(can_msg.get_last_msg().data), length=payload_len_last, offset=0)
            curr_payload_bitarray = BitArray(bytes=bytes(can_msg.get_curr_msg().data), length=payload_len_curr, offset=0)

            for bit_index in range(0, payload_len_last):
                last_bit_value = last_payload_bitarray[bit_index]
                curr_bit_value = curr_payload_bitarray[bit_index]
                transition_aggregation_vector[bit_index] = last_bit_value ^ curr_bit_value

        return transition_aggregation_vector