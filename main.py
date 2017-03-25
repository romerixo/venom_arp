import sys
import color as c
from scapy.all import *

GATEWAY = None
TARGETS = None

def check_args():
    global GATEWAY, TARGETS
    argv = sys.argv[1:]
    argc = len(argv)

    # gateway
    if('-g' in argv):
        index = argv.index('-g') + 1
        if(index < argc):
            GATEWAY = argv[index]

    # targets
    if('-t' in argv):
        index = argv.index('-t') + 1 
        if(index < argc):
            TARGETS = list(argv[index].split(','))

    return (GATEWAY and TARGETS)

def usage():
    print c.ERR + \
'''
Sintaxis error
Usage:
    venom_arp -g <gateway> -t <target_list>
'''

def get_mac(ip):
    global GATEWAY
    result = sr(ARP(op=ARP.who_has, pdst=ip), verbose=False)
    return result[0][ARP][0][1].hwsrc

################################# main #########################################

def main():
    GATEWAY = '192.168.1.1'
    print get_mac('192.168.1.128')

    # if(check_args()):
    #     print get_mac()
    # else:
    #     usage()
    #     sys.exit(1)

if(__name__ == '__main__'):
        main()
