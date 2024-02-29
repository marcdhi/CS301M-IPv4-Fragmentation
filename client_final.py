import socket
import struct
import binascii

# Function to split data into fragments
def split_data_into_fragments(data, max_transmission_unit):
    # Split the data into fragments of size max_transmission_unit - 20
    fragments = [data[i:i+max_transmission_unit-20] for i in range(0, len(data), max_transmission_unit-20)]
    return fragments

# Function to compute checksum
def compute_checksum(data):
    # Compute the checksum using binascii.crc_hqx
    return binascii.crc_hqx(data, 0)

# Function to send a fragment
def transmit_fragment(udp_socket, destination_ip, destination_port, fragment, fragment_index, total_fragments, remaining_fragments, max_transmission_unit):
    # Initialize flag_bits
    flag_bits = 0b0000000000000000
    # Shift remaining_fragments 13 bits to the left
    remaining_fragments = remaining_fragments << 13
    # Compute fragment_offset
    fragment_offset = int((fragment_index*max_transmission_unit)/8)
    # Update flag_bits
    flag_bits = flag_bits | remaining_fragments | fragment_offset
    
    # Compute checksum_value
    checksum_value = int(compute_checksum(struct.pack('!BBHHHBBH', 69, 0, 20 + len(fragment), 0, int(flag_bits), socket.IPPROTO_UDP, 127, 0)+socket.inet_aton(destination_ip)+socket.inet_aton("127.0.0.1")))
    
    # Pack the IPv4 header
    packet_data = struct.pack('!BBHHHBBH', 69, 0, 20 + len(fragment), 0, int(flag_bits), socket.IPPROTO_UDP, 127, checksum_value)
    # Add source IP address
    packet_data += socket.inet_aton(destination_ip)
    # Add destination IP address
    packet_data += socket.inet_aton("127.0.0.1")
    
    # Add the fragment to the packet_data
    packet_data += fragment
    # Send the packet_data
    udp_socket.sendto(packet_data, (destination_ip, destination_port))
    print(f"Fragment {fragment_index + 1} of {total_fragments} sent successfully.")

# Main client function
def udp_client(destination_ip, destination_port, file_path, max_transmission_unit):
    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Open the file in binary mode and read its content
    with open(file_path, 'rb') as file:
        data = file.read()

    # Split the data into fragments
    fragments = split_data_into_fragments(data, max_transmission_unit)
    total_fragments = len(fragments)

    # Transmit each fragment
    for index, fragment in enumerate(fragments):
        remaining_fragments = 1 if index < total_fragments - 1 else 0
        transmit_fragment(udp_socket, destination_ip, destination_port, fragment, index, total_fragments, remaining_fragments, max_transmission_unit)

    # Close the socket
    udp_socket.close()

if __name__ == "__main__":
    file_path = "frag.txt"
    max_transmission_unit = int(input("Enter the Maximum Transmission Unit (MTU) size: "))
    udp_client('127.0.0.1', 3000, file_path, max_transmission_unit)
