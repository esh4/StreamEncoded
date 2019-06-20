from GUI import Pencode
from Tools import monitor_network_activity
import _thread
from scapy.all import sniff
import logging

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    _thread.start_new_thread(sniff, (), {
        'iface': 'lo',
        'filter': 'port 5990',
        'prn': monitor_network_activity})
    Simple = Pencode()
    Simple.wait_for_image()
    Simple.run()

