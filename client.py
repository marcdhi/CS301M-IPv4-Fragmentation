import socket
from scapy.all import *

def send_fragments(filename, dst_ip, dst_port, mtu):
    with open(filename, 'rb') as f:
        data = f.read()

    fragments = fragment(data, mtu)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((dst_ip, dst_port))
        for frag in fragments:
            ip_pkt = IP(dst=dst_ip) / frag
            s.sendall(bytes(ip_pkt))
            print("Sent fragment with IP header:", ip_pkt[IP].summary())

def main():
    filename = "file_to_send.txt"
    dst_ip = "127.0.0.1"
    dst_port = 12345  # Choose any available port on the server
    mtu = 1500  # Set the MTU size
    send_fragments(filename, dst_ip, dst_port, mtu)

if __name__ == "__main__":
    main()
