import socket
import struct
import hashlib

def calculate_checksum(data):
    # Calculate a simple checksum using MD5 hash
    checksum = hashlib.md5(data).hexdigest()
    return checksum

def send_fragmented_data(file_name, mtu):
    with socket.create_connection(("127.0.0.1", 12345)) as stream:
        # Send MTU size as a 4-byte integer
        stream.sendall(struct.pack('!I', mtu))
        print(f"Client: Sent MTU size: {mtu} bytes")

        with open(file_name, "rb") as file:
            buffer = bytearray(mtu)
            fragment_count = 0

            while True:
                bytes_read = file.readinto(buffer)
                if bytes_read == 0:
                    break

                fragment_count += 1
                print(f"Client: Fragmenting data: Fragment {fragment_count}, size = {bytes_read} bytes")

                # Calculate checksum for the fragment
                checksum = calculate_checksum(buffer[:bytes_read])

                # Simulate fragmentation by sending data in chunks of MTU size
                stream.sendall(struct.pack('!I', bytes_read))  # Send fragment size
                stream.sendall(buffer[:bytes_read])  # Send fragment data
                stream.sendall(checksum.encode())  # Send checksum
                print(f"Client: Sent fragment {fragment_count}, checksum: {checksum}")

    print(f"Client: Finished sending {fragment_count} fragments")

def main():
    file_name = "frag.txt"

    # Dynamically ask the user to input the MTU size
    mtu_size_str = input("Enter MTU size: ")
    mtu_size = int(mtu_size_str)

    print(f"Client: Sending file {file_name} with MTU size {mtu_size} bytes")
    send_fragmented_data(file_name, mtu_size)

if __name__ == "__main__":
    main()
