mod server;
mod client;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        println!("Usage: {} <mode>", args[0]);
        return;
    }

    let mode = &args[1];
    match mode.as_str() {
        "server" => server::start_server(),
        "client" => client::start_client(),
        _ => println!("Invalid mode"),
    }
}