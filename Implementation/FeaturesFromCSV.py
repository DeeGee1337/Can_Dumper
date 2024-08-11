from locale import normalize
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from bitstring import BitArray

can_traces = []
available_uds_sessions = [0x1, 0x3, 0x40, 0x4F, 0x60]
for session in available_uds_sessions:
    can_traces.append(pd.read_csv('UDS_Session_' + str(session) + '.csv'))

# create a list for the IDs in the different UDS Sessions
arbitration_id_lists = []
for can_trace in can_traces:
    arbitration_id_list = []
    for index in range(0, 5000):
        arbitration_id = can_trace['Arbitration_ID'][index]
        if arbitration_id not in arbitration_id_list:
            arbitration_id_list.append(arbitration_id)
    arbitration_id_list.sort()
    arbitration_id_lists.append(arbitration_id_list)

# ---------------- calculate frequency of the Messages with the same IDs ---------------- #
def calc_freq(can_traces, available_uds_sessions):
    frequency_list = []
    for can_trace in can_traces:
        frequency = can_trace['Arbitration_ID'].value_counts(normalize=False)
        frequency_list.append(frequency)

    i = 0
    for frequency in frequency_list:
        plt.figure(figsize=(19.20, 10.80))
        frequency.plot(kind='bar')
        plt.xlabel('Arbitration ID')
        plt.ylabel('Frequency')
        plt.title('Frequency of Messages with the same Arbitration ID in the UDS Session ' + str(available_uds_sessions[i]))
        plt.savefig('Frequency_UDS_Session ' + str(available_uds_sessions[i]) + '.png', dpi=700, bbox_inches='tight')
        i = i + 1

def calc_normalized_freq(can_traces, available_uds_sessions):
    normalize_frequency_list = []
    for can_trace in can_traces:
        normalize_frequency = can_trace['Arbitration_ID'].value_counts(normalize=True)
        normalize_frequency_list.append(normalize_frequency)

    i = 0
    for normalize_frequency in normalize_frequency_list:
        plt.figure(figsize=(19.20, 10.80))
        normalize_frequency.plot(kind='bar')
        plt.xlabel('Arbitration ID')
        plt.ylabel('Normalized Frequency')
        plt.title('Normalized Frequency of Messages with the same Arbitration ID in the UDS Session ' + str(available_uds_sessions[i]))
        plt.savefig('Normalized_Frequency_UDS_Session ' + str(available_uds_sessions[i]) + '.png', dpi=700, bbox_inches='tight')
        i = i + 1

# ---------------- calculate the Transition Aggregation Vector ---------------- #
for session_index in range(0, len(can_traces)):
    for arbitration_id in arbitration_id_lists[session_index]:
        can_trace_per_id = can_traces[session_index].loc[can_traces[session_index]['Arbitration_ID'] == arbitration_id]
        can_trace_per_id.reset_index(inplace=True, drop=True)
        transition_aggregation_vector = [0] * 64#(can_trace_per_id['Data_Length_Code'].iloc[0])

        for index in range(1, len(can_trace_per_id.index)):
            last_payload = can_trace_per_id['Payload'][index-1]
            last_payload_bitarray = BitArray(bytes=bytes(last_payload, 'utf-8'), length=can_trace_per_id['Data_Length_Code'][index-1])

            curr_payload = can_trace_per_id['Payload'][index]
            curr_payload_bitarray = BitArray(bytes=bytes(curr_payload, 'utf-8'), length=can_trace_per_id['Data_Length_Code'][index])

            size = min(can_trace_per_id['Data_Length_Code'][index], can_trace_per_id['Data_Length_Code'][index-1])
            for bit_index in range(0, size):
                last_bit_value = last_payload_bitarray[bit_index]
                curr_bit_value = curr_payload_bitarray[bit_index]
                transition_aggregation_vector[bit_index] = transition_aggregation_vector[bit_index] + (last_bit_value ^ curr_bit_value)

        print('ID ' + str(arbitration_id) + ': ' + str(transition_aggregation_vector))
            

