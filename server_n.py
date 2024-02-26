import socket
import struct

def receive_fragmented_data(stream, file_name):
    with open(file_name, 'wb') as file:
        # Receive the 4-byte integer representing the MTU size
        mtu_size_bytes = stream.recv(4) # size of an integer in bytes which is 4
        
        # Unpack the received bytes into an integer (assumes network byte order, '!')
        mtu_size = struct.unpack('!I', mtu_size_bytes)[0]
        print(f"Server: Received MTU size of {mtu_size} bytes")

        fragment_number = 1

        while True:
            buffer = stream.recv(mtu_size)
            if not buffer:
                break

            file.write(buffer)
            bytes_read = len(buffer)
            print(f"Server: Received Fragment {fragment_number} of size {bytes_read} bytes")
            fragment_number += 1

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(('127.0.0.1', 12345))
        listener.listen()

        print("Server: Started and listening on 127.0.0.1:12345")

        stream, _ = listener.accept()
        print("Server: Connection established with client")

        file_name = "received_file.txt"
        receive_fragmented_data(stream, file_name)

        print(f"Server: File '{file_name}' received and saved successfully")

def main():
    start_server()

if __name__ == "__main__":
    main()
