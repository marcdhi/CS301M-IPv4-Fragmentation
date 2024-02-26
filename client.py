import socket

def send_fragmented_data(file_name, mtu):
    with socket.create_connection(("127.0.0.1", 12345)) as stream:
        with open(file_name, "rb") as file:
            buffer = bytearray(mtu)

            while True:
                bytes_read = file.readinto(buffer)
                print(f"bytes=",bytes_read)
                if bytes_read == 0:
                    break
                stream.sendall(buffer[:bytes_read])

def main():
    file_name = "frag.txt"

    # Dynamically ask the user to input the MTU size
    mtu_size_str = input("Enter MTU size: ")
    mtu_size = int(mtu_size_str)

    send_fragmented_data(file_name, mtu_size)

if __name__ == "__main__":
    main()
