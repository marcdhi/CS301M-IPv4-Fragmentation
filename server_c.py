import socket
import struct
import hashlib

def calculate_checksum(data):
    # Calculate a simple checksum using MD5 hash
    checksum = hashlib.md5(data).hexdigest()
    return checksum

def receive_fragmented_data(stream, file_name):
    with open(file_name, 'wb') as file:
        # Receive the 4-byte integer representing the MTU size
        mtu_size_bytes = stream.recv(4)  # size of an integer in bytes which is 4
        
        # Unpack the received bytes into an integer (assumes network byte order, '!')
        mtu_size = struct.unpack('!I', mtu_size_bytes)[0]
        print(f"Server: Received MTU size of {mtu_size} bytes")

        fragment_number = 1

        while True:
            # Receive the size of the next fragment
            try:
                fragment_size_bytes = stream.recv(4)
                fragment_size = struct.unpack('!I', fragment_size_bytes)[0]
            except struct.error:
                break

            if fragment_size == 0:
                break

            # Receive the fragment data
            buffer = stream.recv(fragment_size)

            # Receive the checksum
            checksum_received = stream.recv(32).decode()

            # Calculate checksum for the received fragment
            checksum_calculated = calculate_checksum(buffer)

            # Verify checksum
            if checksum_received == checksum_calculated:
                print(f"Server: Received Fragment {fragment_number} of size {fragment_size} bytes, checksum verified")
                file.write(buffer)
            else:
                print(f"Server: Error in Fragment {fragment_number}: Checksum mismatch")

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
