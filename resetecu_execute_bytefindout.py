from scapy.all import *
import time

conf.contribs['CANSocket'] = {'use-python-can': False}
load_contrib("cansocket")
load_layer("can")

sock = CANSocket(channel='can1')
m = 549439154539200512 #00
#m = 549440254050828288 #01
#m = 549441353562456064 #02
#m = 549442453074083840 #03
#m = 0

# Define the initial values
first_bytes = [0x07, 0xA0]
bytes_rest = [0x00, 0x00, 0x00, 0x00, 0x00]

# Iterate my_byte from 0x00 to 0xFF
for i in range(0, 256):
    my_byte = [i]
    
    payload = bytes(first_bytes + my_byte + bytes_rest)
    
    print("current byte:", payload)

    frame = CAN(flags='extended', identifier=402190963, length=8, data=payload)
    sock.send(frame)
    # frame.show()
    time.sleep(20)
    print("20s delay done..")
    # time.sleep(0.001)

print("done")
