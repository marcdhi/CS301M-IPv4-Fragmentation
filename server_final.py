import socket
import struct
import os
import shutil
        
def start_server(server_ip, server_port,folder_name):

    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)
    os.mkdir(folder_name)

    # Create a server socket
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the server socket to the specified IP and port
    udp_server_socket.bind((server_ip, server_port))
    print(f"Server started on {server_ip}:{server_port}")
    received_message = ""
    transmission_info = f"Server started on {server_ip}:{server_port}\n"
    packet_count = 0
    while True:
        # Receive data from the client
        packet_data, client_addr = udp_server_socket.recvfrom(1024)
        # Unpack the IPv4 header
        unpacked_header = struct.unpack('!BBHHHBBH', packet_data[:12])  

        # Extract various fields from the header
        ip_version = unpacked_header[0] >> 4  
        header_length = (unpacked_header[0] & 0xF) * 4  
        service_type = (unpacked_header[1] >> 2)  
        packet_length = unpacked_header[2]  
        packet_id = unpacked_header[3]  
        packet_flags = (unpacked_header[4] >> 13) & 0x7  
        fragment_offset = unpacked_header[4] & 0x1FFF  
        transport_protocol = unpacked_header[5]  
        time_to_live = unpacked_header[6]  
        header_checksum = hex(unpacked_header[7])  
        source_ip = socket.inet_ntoa(bytes(struct.unpack('!BBBB', packet_data[12:16])))  
        destination_ip = socket.inet_ntoa(bytes(struct.unpack('!BBBB', packet_data[16:20])))  
        packet_payload = packet_data[20:]  

        transmission_info += "\n"
        transmission_info += f"Received IPv4 packet from {client_addr}\n"
        transmission_info += f"IP Version: {ip_version}, Header Length: {header_length} bytes\n"
        transmission_info += f"Service Type: {service_type}, Packet Length: {packet_length}\n"
        transmission_info += f"Packet ID: {packet_id}, Flags: {packet_flags}, Fragment Offset: {fragment_offset}\n"
        transmission_info += f"Time to Live: {time_to_live}, Protocol: {transport_protocol}, Checksum: {header_checksum}\n"
        transmission_info += f"Source IP: {source_ip}, Destination IP: {destination_ip}\n"
        transmission_info += f"Payload: {packet_payload}\n"
        received_message += packet_payload.decode('utf-8')

        # Write the received message to a file
        with open(f'reassembled_{packet_count}.txt', 'w') as output_file:
            output_file.write(received_message)

        # Write the transmission info to a file
        with open(f'{folder_name}/transmission_info_{packet_count}.txt', 'w') as info_file:
            info_file.write(transmission_info)

        packet_count += 1
        if packet_flags == 0:
            break
    udp_server_socket.close()

if __name__ == "__main__":
    folder_name = "fragmentations"
    start_server('127.0.0.1', 3000, folder_name)
