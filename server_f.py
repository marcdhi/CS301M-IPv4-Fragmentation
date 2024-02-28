import os
import socket
import struct
import hashlib
import shutil

def ipv4_header(data):
    ip_header = struct.unpack('!BBHHHBBH4s4s', data[:20])
    version_ihl = ip_header[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF
    ttl = ip_header[5]
    protocol = ip_header[6]
    src_ip = socket.inet_ntoa(ip_header[8])
    dest_ip = socket.inet_ntoa(ip_header[9])
    return ip_header, version_ihl, version, ihl, ttl, protocol, src_ip, dest_ip

# Function to calculate checksum
def calculate_checksum(data):
    checksum = hashlib.md5(data).hexdigest()
    return checksum

# Function to receive fragmented data
def receive_fragmented_data(stream, folder_name):

    # Receive MTU size
    mtu_size_bytes = stream.recv(4)
    mtu_size = struct.unpack('!I', mtu_size_bytes)[0]

    # Create folder for fragmentations if it doesn't exist, or delete and remake if it exists
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)
    os.mkdir(folder_name)

    fragment_number = 1
    reassembled_data = b''  # Initialize empty reassembled data buffer

    while True:
        try:
            # Receive fragment size
            fragment_size_bytes = stream.recv(4)
            fragment_size = struct.unpack('!I', fragment_size_bytes)[0]
        except struct.error:
            break

        if fragment_size == 0:
            break

        buffer = stream.recv(fragment_size)
        # Receive checksum
        checksum_received = stream.recv(32).decode()
        # Calculate checksum for the received data
        checksum_calculated = calculate_checksum(buffer)

        # Verify checksum
        if checksum_received == checksum_calculated:
            print(f"Server: Received Fragment {fragment_number} of size {fragment_size} bytes, checksum verified")

            ip_header, version_ihl, version, ihl, ttl, protocol, src_ip, dest_ip = ipv4_header(buffer)

            # Write IPv4 header information to a separate file or append it to the reassembled file
            header_info_file_name = os.path.join(folder_name, f"ipv4_header_{fragment_number}_info.txt")
            with open(header_info_file_name, 'wb') as header_info_file:
                header_info_file.write(f"Fragment Number: {fragment_number}\n".encode())
                header_info_file.write(f"Version: {version}\n".encode())
                header_info_file.write(f"IHL: {ihl}\n".encode())
                header_info_file.write(f"TTL: {ttl}\n".encode())
                header_info_file.write(f"Protocol: {protocol}\n".encode())
                header_info_file.write(f"Source IP: {src_ip}\n".encode())
                header_info_file.write(f"Destination IP: {dest_ip}\n\n".encode())

                header_info_file.write(f"------Fragmented Data------\n\n".encode())

                # Write fragment data to the file
                header_info_file.write(buffer)
            # Append fragment to reassembled data
            reassembled_data += buffer
        else:
            print(f"Server: Error in Fragment {fragment_number}: Checksum mismatch")

        fragment_number += 1


    ip_header, version_ihl, version, ihl, ttl, protocol, src_ip, dest_ip = ipv4_header(reassembled_data)

    # Write reassembled data to a file
    reassembled_file_name = os.path.join(folder_name, "received_frags.txt")
    with open(reassembled_file_name, 'wb') as reassembled_file:
        reassembled_file.write(f"Version: {version}\n".encode())
        reassembled_file.write(f"IHL: {ihl}\n".encode())
        reassembled_file.write(f"TTL: {ttl}\n".encode())
        reassembled_file.write(f"Protocol: {protocol}\n".encode())
        reassembled_file.write(f"Source IP: {src_ip}\n".encode())
        reassembled_file.write(f"Destination IP: {dest_ip}\n\n".encode())

        reassembled_file.write(f"------Final Received Data------\n\n".encode())
    
        reassembled_file.write(reassembled_data)

    print(f"Server: Fragmented files received and saved successfully in folder '{folder_name}'")

# Function to start the server
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(('127.0.0.1', 12345))
        listener.listen()

        print("Server: Started and listening on 127.0.0.1:12345")

        stream, _ = listener.accept()
        print("Server: Connection established with client")

        folder_name = "fragmentations"
        receive_fragmented_data(stream, folder_name)

# Main function
def main():
    start_server()

if __name__ == "__main__":
    main()
