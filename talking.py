import socket, threading, time, platform, sys

# ------------------ CONFIG ------------------
UDP_PORT = 50700
TCP_PORT = 50701

# ------------------ NAME INPUT ------------------
default_name = platform.node() or "PC"
print(f"Name [{default_name}]: ", end="", flush=True)
name = sys.stdin.readline().strip() or default_name

# ------------------ PEER STORAGE ------------------
peers = {}
lock = threading.Lock()

# ------------------ UDP DISCOVERY ------------------
def broadcast():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        s.sendto(f"DISCOVER|{name}|{TCP_PORT}".encode(), ("255.255.255.255", UDP_PORT))
        time.sleep(2)

def listen_discovery():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", UDP_PORT))
    while True:
        try:
            data, addr = s.recvfrom(1024)
            tag, peer_name, port = data.decode().split("|")
            if tag == "DISCOVER" and peer_name != name:
                with lock:
                    peers[peer_name] = (addr[0], int(port))
        except:
            continue

# ------------------ CHAT ------------------
def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(f"\n{msg}")
        except:
            break

def chat(sock):
    threading.Thread(target=receive, args=(sock,), daemon=True).start()
    while True:
        try:
            msg = input()
            sock.send(f"{name}: {msg}".encode())
        except:
            break

# ------------------ SERVER ------------------
def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", TCP_PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        try:
            peer_name = conn.recv(1024).decode()
        except:
            conn.close()
            continue

        print(f"\n{peer_name} wants to chat from {addr[0]}.")
        if input("Allow? (y/n): ").lower() != "y":
            conn.close()
            continue

        conn.send(b"OK")
        print("Connected!\n")
        chat(conn)

# ------------------ CLIENT ------------------
def connect_to_peer(ip=None, port=None):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.send(name.encode())
        if s.recv(1024).decode() == "OK":
            print("Connected!\n")
            chat(s)
    except Exception as e:
        print(f"Connection failed: {e}")

def client_menu():
    while True:
        print("\nChoose connection mode:")
        print("1) LAN discovery (auto detect peers)")
        print("2) IPv4 / port manually")
        mode = input("Mode (1 or 2): ").strip()
        if mode == "1":
            while True:
                time.sleep(2)
                with lock:
                    if not peers:
                        print("Looking for LAN peers...")
                        continue
                    print("\nComputers found:")
                    names = list(peers.keys())
                    for i, n in enumerate(names, 1):
                        print(f"{i}) {n}")
                choice = input("Select number (Enter to refresh, q to go back): ").strip()
                if choice.lower() == "q":
                    break
                if not choice:
                    continue
                try:
                    ip, port = peers[names[int(choice)-1]]
                    connect_to_peer(ip, port)
                except:
                    print("Connection failed")
        elif mode == "2":
            ip = input("Enter IPv4 address of peer: ").strip()
            port = int(input("Enter port: ").strip())
            connect_to_peer(ip, port)
        else:
            print("Invalid option")

# ------------------ START ------------------
threading.Thread(target=broadcast, daemon=True).start()
threading.Thread(target=listen_discovery, daemon=True).start()
threading.Thread(target=server, daemon=True).start()

client_menu()
