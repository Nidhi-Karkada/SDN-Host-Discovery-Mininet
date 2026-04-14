# SDN Host Discovery & Traffic Control (POX + Mininet)

##  Problem Statement
This project implements an SDN-based solution using POX and Mininet to:
- Detect host join events
- Maintain a host database
- Apply traffic control using OpenFlow rules

---

##  Setup & Execution

### Step 1: Clone Repository
git clone https://github.com/Nidhi-Karkada/SDN-Host-Discovery-Mininet.git
cd SDN-Host-Discovery-Mininet

### Step 2: Start Controller
cd pox
./pox.py openflow.of_01 host_discovery log.level --DEBUG

### Step 3: Start Mininet
sudo mn --controller=remote --topo single,3

---

##  Testing

### Run:
pingall

h1 ping h2

h1 ping h3

---

## Expected Output

- h1 → h2  (Blocked)
- h1 → h3  (Allowed)

---

##  Proof of Execution

### 🔹 Flow Table
sudo ovs-ofctl dump-flows s1

### 🔹 Wireshark
- Interface: any
- Filter: icmp

---

##  Screenshots

### Blocked Traffic
![Blocked](screenshots/blocked.png)

### Allowed Traffic
![Allowed](screenshots/allowed.png)

### Flow Table
![Flows](screenshots/flows.png)

---

## Tools Used
- Mininet
- POX Controller
- Wireshark
- OpenFlow

---

## Author
Nidhi Karkada
