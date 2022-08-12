#This file expects to be run with one argument, the name of network namespace to be created.
#This script also expects access to a file with a number 0-9 inclusive which is used to make sure that no two namespaces that it creats attempt to use the same ip addresses.
#The ip assignment system here IS NOT IDIOT PROOF and will break if you have anything else runnign on the ip adresses it uses by default or if you, for some reason, have made more than 10 network namspaces with this script without deleting any.

import os
import sys

def command(arg):
    argument = arg
    print(argument)
    stream = os.popen(arg)
    output = stream.read()
    if ((len(output) > 1) and (output != "1\n")):
        print(output)

def main(name):
    os.chdir("/home/monkey/Software/PythonScripts/NetnsCreator/")

    with open("lastIp") as file:
        lastIp = int(file.read().strip())

    if lastIp == 9:newIp = 0
    else:newIp = lastIp + 1

    with open("lastIp", "a") as file:
        file.truncate(0)
        file.write(str(newIp))

    ip1 = "10.0." + str(10 + lastIp) + ".1"
    ip2 = "10.0." + str(10 + lastIp) + ".2"

    command("sudo ip netns add " + name)
    command("sudo ip netns exec " + name + " ip link set dev lo up")
    command("sudo ip link add " + name + "veth0 type veth peer name " + name + "veth1")
    command("sudo ip link set dev " + name + "veth1 netns " + name)
    command("sudo ip a a " + ip1 + "/24 dev " + name + "veth0")
    command("sudo ip netns exec " + name + " ip a a " + ip2 + "/24 dev " + name + "veth1")
    command("sudo ip link set dev " + name + "veth0 up")
    command("sudo ip netns exec " + name + " ip link set dev " + name + "veth1 up")
    command("echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward")
    command("sudo iptables -A FORWARD -o enp2s0 -i " + name + "veth0 -j ACCEPT")
    command("sudo iptables -A FORWARD -i enp2s0 -o " + name + "veth0 -j ACCEPT")
    command("sudo iptables -t nat -A POSTROUTING -s " + ip2 + "/24 -o enp2s0 -j MASQUERADE")
    command("sudo ip netns exec " + name + " ip route add default via " + ip1)

if __name__ == "__main__": main(sys.argv[1:][0])
