import socket

def receive_fragmented_data(stream, file_name):
    with open(file_name, 'wb') as file:
        buffer_size = 1
        fragment_number = 1

        while True:
            buffer = stream.recv(buffer_size)
            if not buffer:
                break

            file.write(buffer)
            bytes_read = len(buffer)
            print(f"Received Fragment {fragment_number}, Size: {bytes_read} bytes")
            fragment_number += 1

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(('127.0.0.1', 12345))
        listener.listen()

        print("Server listening on 127.0.0.1:12345")

        stream, _ = listener.accept()
        print("Connection established")

        file_name = "received_file.txt"
        receive_fragmented_data(stream, file_name)

        print(f"File '{file_name}' received successfully")

def main():
    start_server()

if __name__ == "__main__":
    main()
