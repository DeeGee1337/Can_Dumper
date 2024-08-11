from multiprocessing.spawn import import_main_path
import scapy.all as scapy
import scapy.config as config
from scapy.layers import can
from scapy.contrib import cansocket,isotp,automotive
from scapy.contrib.automotive import uds, uds_scan
config.conf.contribs['CANSocket'] = {'use-python-can': False}
config.conf.contribs['ISOTP'] = {'use-can-isotp-kernel-module': True}

import time 

class DiagFunctions:
    def __init__(self, interface="can0"):
        self.interface = interface
        self.socket = cansocket.CANSocket(self.interface)#,can_filters=[{'can_id': 0x7dd, 'can_mask': 0x7FF}])
        self.isotpsocket = isotp.ISOTPSocket(self.socket, tx_id=0x773 , rx_id=0x7dd, basecls = uds.UDS, padding = True)
    def scan(self):
        isotpsockets = isotp.ISOTPScan(sock=self.socket, scan_range=range(0x700, 0x800), can_interface=self.interface, verbose=True)
        for sockettest in isotpsockets:
            sockettest.basecls = uds.UDS
            sockettest.padding = True
            print("Test ISOTP socket sid=0x%x, did=0x%x" % (sockettest.src, sockettest.dst))
            resp = sockettest.sr1(uds.UDS() / uds.UDS_DSC(diagnosticSessionType=3), timeout=1, verbose=False)
            if resp is None:
                print("Error: UDS not supported")
                continue
            elif resp.service == 0x50 or resp.service == 0x7f:
                print("UDS supported")

    def setsession(self,session=0x1):
        # Test if ISOTP Socket supports UDS (Long Timeout)
        resp = self.isotpsocket.sr1(uds.UDS() / uds.UDS_DSC(diagnosticSessionType=session), timeout=1, verbose=False)
        if resp is None:
            print("Error UDS Session not reached")
        elif resp.service == 0x50:
            print("UDS State Changed to: "+ hex(session) + " Sending Tester Present")
            self.tester = uds.UDS_TesterPresentSender(self.isotpsocket)
            self.tester.start()
        else:
            print(resp)
            print("Error UDS Session not changed")
    def endsession(self):
        print("Stop Tester Present")
        self.tester.stop()
    def closesockets(self):
        self.isotpsocket.close()
        self.socket.close()
    def opensockets(self):
        self.socket = cansocket.CANSocket(channel=self.interface,can_filters=[{'can_id': 0x7dd, 'can_mask': 0x7FF}])
        self.isotpsocket = isotp.ISOTPSocket(self.socket, sid=0x773, did=0x7dd, basecls=uds.UDS, padding=True)


#diag = DiagFunctions()
#diag.setsession(0x3)