import color as c
print c.INFO + 'Loading modules...' + c.CLR
import sys
import re
from scapy.all import sr, ARP

GATEWAY = None
TARGET = None

# TODO: target -> range, ip_list

# ip in format 'xxx.xxx.xxx.xxx'
def _ip_next(ip):
    # convert in int
    ip = ip.split('.')
    for i, ip_sec in enumerate(ip):
        ip[i] = int(ip_sec)

    if(ip[3] < 255):
        ip[3] += 1
    elif(ip[2] < 255):
        ip[3] = 1
        ip[2] += 1
    elif(ip[1] < 255):
        ip[3] = 1
        ip[2] = 1
        ip[1] += 1
    elif(ip[0] < 255):
        ip[3] = 1
        ip[2] = 1
        ip[1] = 1
        ip[0] += 1
    
    # convert to str
    for i, ip_sec in enumerate(ip):
        ip[i] = str(ip_sec)

    return '.'.join(ip)
    
def _get_range(ip_range):
    ips = []
    
    ip_start = ip_range.split('-')[0]
    ip_end = ip_range.split('-')[1]

    ips.append(ip_start)
   
    while(ips[-1] != ip_end):
        ips.append(_ip_next(ips[-1]))

    return ips

def _is_ip(ip):
    pattern = '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|\
[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'

    return re.match(pattern, ip)

def check_args():
    global TARGET, GATEWAY

    if(len(sys.argv) == 3):
        if(_is_ip(sys.argv[1])):
            GATEWAY = sys.argv[1]

        # target
        for c in sys.argv[2]:
            if(c == '-'):
                TARGET = _get_range(sys.argv[2])
                break
            else:
                TARGET = sys.argv[2].split(',')
        for ip in TARGET:
            if(not _is_ip(ip)):
                TARGET = None
                break

    return (GATEWAY and TARGET)

def usage():
    print c.ERR + \
'''
Sintaxis error
Usage:
    venom_arp <ip_gateway> (<ip_target> | <ip_list> | <ip_range>)
'''

def get_mac(ip):
    global GATEWAY
    mac = None
    
    try:
        result = sr(ARP(op=ARP.who_has, pdst=ip), verbose=False, timeout=0.5)
        mac = result[0][ARP][0][1].hwsrc
    except:
        pass

    return mac

################################# main #########################################

def main():
    global TARGET, GATEWAY
# Geting MAC for IP 192.168.1.100 ...
    if(check_args()):
        # try:
        print c.PROM + '      IP                  MAC'
        for ip in TARGET:
            print c.OK + '{}      {}'.format(ip, get_mac(ip))
        # except Exception as e:
        #     print c.ERR + str(e)

    else:
        usage()
        return -1

if(__name__ == '__main__'):
        print 'Before'
        main()
