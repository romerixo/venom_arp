import sys
import color as c

HELP = \
'''
Sintaxis error
Usage:
    venom_arp -g <gateway> -t <target_list>
'''
def set_arguments():
    ARGC = len(sys.argv)
    GATEWAY = None
    TARGETS = None

    # gateway
    if('-g' in sys.argv):
        index = sys.argv.index('-g') + 1
        if(index < ARGC):
            GATEWAY = sys.argv[index]

    # targets
    if('-t' in sys.argv):
        index = sys.argv.index('-t') + 1
        if(index < ARGC):
            TARGETS = list(sys.argv[index].split(','))

    return (GATEWAY and TARGETS)

def main():
    if(set_arguments()):
        print c.ok('[*] Todo bien, todo correcto')
    else:
        print c.err(HELP)
        sys.exit(1)

if(__name__ == '__main__'):
    main()
