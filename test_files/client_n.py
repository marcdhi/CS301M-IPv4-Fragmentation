import socket
import struct
def send_fragmented_data(file_name, mtu):
    with socket.create_connection(("127.0.0.1", 12345)) as stream:
        # Send MTU size as a 4-byte integer
        stream.sendall(struct.pack('!I', mtu))
        print(f"Sent MTU size: {mtu}")

        with open(file_name, "rb") as file:
            buffer = bytearray(mtu)
            fragment_count = 0

            while True:
                bytes_read = file.readinto(buffer)
                if bytes_read == 0:
                    break
                fragment_count += 1
                print(f"Fragmenting data: Fragment {fragment_count} size = {bytes_read} bytes")
                stream.sendall(buffer[:bytes_read])
                print(f"Sent fragment {fragment_count}")

    print(f"Finished sending {fragment_count} fragments")

def main():
    file_name = "frag.txt"

    # Dynamically ask the user to input the MTU size
    mtu_size_str = input("Enter MTU size: ")
    mtu_size = int(mtu_size_str)

    print(f"Sending file {file_name} with MTU size {mtu_size}")
    send_fragmented_data(file_name, mtu_size)

if __name__ == "__main__":
    main()
