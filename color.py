from colorama import init, Fore, Style

init()

WARN = Fore.YELLOW + Style.BRIGHT
OK = Fore.GREEN + Style.BRIGHT
ERR = Fore.RED + Style.BRIGHT
PROM = Fore.MAGENTA + Style.BRIGHT
CLR = Fore.RESET + Style.RESET_ALL

def ok(txt):
    return OK + txt + CLR
def err(txt):
    return ERR + txt + CLR
def prom(txt):
    return PROM + txt + CLR
