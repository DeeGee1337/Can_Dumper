import can
import os

# Configuration of the CAN-Parser
CAN_INTERFACE = 'socketcan'
CAN_CHANNEL = 'can1'
CAN_STATE = can.bus.BusState.PASSIVE
CAN_BITRATE = 500000


class CANInterface:
    def __init__(self, interface, channel, bitrate, state):
        self.__interface = interface
        self.__channel = channel
        self.__bitrate = bitrate
        self.__state = state

        # Configurate and create CAN Object
        if interface == 'socketcan':
            self.__start_socketCAN()

        self.__config_can()
        self.__can_bus = can.Bus()

    def __start_socketCAN(self):
        # Systemcall for add peak_usb to the Linux kernel
        os.system('sudo modprobe peak_usb')

        # Systemcall for deactivation of Linux SocketCAN ip link
        os.system('sudo ip link set ' + self.__channel + ' down')

        # Systemcall for activation of Linux SocketCAN ip link
        os.system('sudo ip link set up ' + self.__channel + ' type can bitrate ' + str(self.__bitrate))    
    
    def __config_can(self):
        '''
        Configure the CAN Object from python-can.
        '''
        can.rc['interface'] = self.__interface
        can.rc['channel'] = self.__channel
        can.rc['state'] = self.__state
        can.rc['bitrate'] = self.__bitrate

    def receive(self):
        recv_message = self.__can_bus.recv()
        return recv_message


