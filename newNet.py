import os

def command(arg):
    stream = os.popen(arg)
    output = stream.read()
    if ((len(output) > 1) and (output != "1\n")): print(output)

def main():
    #I may in future add kwargs to change these, but until then they stay
    name = "TTUnet"
    ip1 = "10.0.2.1"
    ip2 = "10.0.2.2"

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
    command("sudo iptables -A FORWARD -o wgivpn -i " + name + "veth0 -j ACCEPT")
    command("sudo iptables -A FORWARD -i wgivpn -o " + name + "veth0 -j ACCEPT")
    command("sudo iptables -t nat -A POSTROUTING -s " + ip2 + "/24 -o enp2s0 -j MASQUERADE")
    command("sudo iptables -t nat -A POSTROUTING -s " + ip2 + "/24 -o wgivpn -j MASQUERADE")
    command("sudo ip netns exec " + name + " ip route add default via " + ip1)

if __name__ == "__main__": main()
