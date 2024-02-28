# IPv4 Fragmentation

## File Structure Info:

1. `client_n.py` & `server_n.py` -> Has code to normally send files and store a single received file
2. `client_c.py` & `server_c.py`-> Has code to verify by hashing the data using hashlib md5 send files, store a single received file, along with verifying the hashed data, to avoid data tampering
3. `client_f.py` & `server_f.py`-> Has code to also have the IPv4 header information, stored into separate fragmented files, along with the final reassembled file.

## Final Output:

<img width="1708" alt="Screenshot 2024-02-28 at 20 41 43" src="https://github.com/marcdhi/CS301M-IPv4-Fragmentation/assets/97223188/63a26e7a-4d01-4bfd-af22-814724c02623">


### **1. Maximum Transmission Unit (MTU):**
MTU refers to the maximum size of a single data packet that can be transmitted over a network. Different networks or network technologies have different MTU sizes. When data needs to be sent across a network, it must be broken down into smaller pieces (fragments) if it exceeds the MTU size of that network.

### **2. Fragmentation:**
Fragmentation is the process of breaking a large data packet into smaller fragments to fit within the MTU of the network. This process occurs at the network layer (Layer 3) of the OSI model.

Here's a simplified overview of how fragmentation works:

- **Sender (Client):**
  1. The sender determines the MTU size of the network it will be transmitting data over.
  2. It breaks down the data into smaller fragments, ensuring that each fragment does not exceed the MTU size.
  3. Each fragment is sent separately to the destination.

- **Network:**
  1. Fragments traverse the network independently, potentially taking different routes to reach the destination.
  2. Routers along the way may handle and forward each fragment.

- **Receiver (Server):**
  1. Fragments arrive at the destination.
  2. The receiver reassembles the fragments into the original data based on information in the packet headers.

### **3. Significance of MTU Size:**
The MTU size is crucial because it determines the maximum size of a packet that can be transmitted without fragmentation. If a packet size exceeds the MTU, it must be fragmented before transmission. Smaller MTU sizes can result in more frequent fragmentation, potentially impacting network performance.

Conversely, a larger MTU size can reduce the need for fragmentation but may lead to increased latency if the network has a mix of smaller MTU devices.

### **4. Data fragments:**
The reported fragment sizes in the output include both the data and any protocol-related overhead associated with each fragment. In our case, even with an MTU size set to 1, the reported fragment sizes are greater than 1 byte, suggesting that each fragment includes additional protocol-related information.
