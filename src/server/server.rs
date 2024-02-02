use std::net::{TcpListener, TcpStream};
use std::io::{Read, Write};
use std::fs::File;

fn receive_fragmented_data(mut stream: TcpStream, file_name: &str) {
    let mut file = File::create(file_name).expect("Failed to create file");
    let mut buffer = [0; 1024];
    let mut fragment_number = 1;

    loop {
        let bytes_read = stream.read(&mut buffer).expect("Failed to read data");
        if bytes_read == 0 {
            break;
        }

        file.write_all(&buffer[..bytes_read]).expect("Failed to write to file");
        println!("Received Fragment {}, Size: {} bytes", fragment_number, bytes_read);
        fragment_number += 1;
    }
}

fn start_server() {
    let listener = TcpListener::bind("127.0.0.1:12345").expect("Failed to bind to address");

    println!("Server listening on 127.0.0.1:12345");

    if let Ok((stream, _)) = listener.accept() {
        println!("Connection established");

        let file_name = "received_file.txt";
        receive_fragmented_data(stream, file_name);

        println!("File '{}' received successfully", file_name);
    }
}

fn main() {
    start_server();
}
