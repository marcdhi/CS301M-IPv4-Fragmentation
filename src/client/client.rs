use std::io::{self, Write};
use std::net::TcpStream;
use std::io::{Read};
use std::fs::File;

fn send_fragmented_data(file_name: &str, mtu: usize) {
    let mut stream = TcpStream::connect("127.0.0.1:12345").expect("Failed to connect to server");
    let mut file = File::open(file_name).expect("Failed to open file");
    let mut buffer = vec![0; mtu];

    while let Ok(bytes_read) = file.read(&mut buffer) {
        if bytes_read == 0 {
            break;
        }
        stream.write_all(&buffer[..bytes_read]).expect("Failed to send data");
    }
}

fn main() {
    let file_name = "frag.txt";

    // Dynamically ask the user to input the MTU size
    let mut mtu_size_str = String::new();
    print!("Enter MTU size: ");
    io::stdout().flush().unwrap();
    io::stdin().read_line(&mut mtu_size_str).expect("Failed to read input");
    let mtu_size: usize = mtu_size_str.trim().parse().expect("Invalid input for MTU size");

    send_fragmented_data(file_name, mtu_size);
}
