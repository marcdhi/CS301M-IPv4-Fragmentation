import socket
from scapy.all import *

def receive_fragments(conn):
    fragments = []
    while True:
        data = conn.recv(4096)
        if not data:
            break
        pkt = IP(data)
        fragments.append(pkt.payload)

        print("Received fragment with IP header:", pkt.summary())

        if pkt.frag == 0:
            break

    return b"".join(fragments)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 12345))  # Use any available port on the server
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            received_data = receive_fragments(conn)
            with open("reassembled_file.txt", "wb") as f:
                f.write(received_data)
            print("Reassembled file saved as reassembled_file.txt")

if __name__ == "__main__":
    main()
