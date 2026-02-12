import socket
import threading
import json
import os
from network import start_lan_listener, connect_direct
from friends import FriendManager
from utils import get_local_ip, generate_friend_code

CONFIG_FILE = "config.json"
DEFAULT_PORT = 5555


def load_config():
    if not os.path.exists(CONFIG_FILE):
        config = {
            "name": socket.gethostname(),
            "friend_code": generate_friend_code()
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        return config
    else:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)


def chat_session(conn, addr):
    print(f"\nConnected to {addr}")
    print("Type /exit to leave chat\n")

    def receive():
        while True:
            try:
                msg = conn.recv(1024).decode()
                if not msg:
                    break
                print(f"\nFriend: {msg}")
            except:
                break

    threading.Thread(target=receive, daemon=True).start()

    while True:
        msg = input("You: ")
        if msg == "/exit":
            break
        conn.send(msg.encode())

    conn.close()


def main():
    config = load_config()
    friend_manager = FriendManager()

    print("\n=== TERMINAL MESSENGER ===")
    print(f"Name: {config['name']}")
    print(f"Your Friend Code: {config['friend_code']}")
    print(f"Your Local IP: {get_local_ip()}")
    print("\n1) Host LAN Chat")
    print("2) Connect LAN Auto")
    print("3) Direct Connect (Off-Network)")
    print("4) Add Friend")
    print("5) Show Friends")

    choice = input("\nChoose: ")

    if choice == "1":
        start_lan_listener(DEFAULT_PORT, chat_session)

    elif choice == "2":
        start_lan_listener(DEFAULT_PORT, chat_session)

    elif choice == "3":
        ip = input("Enter IP: ")
        port = input(f"Port (default {DEFAULT_PORT}): ")
        port = int(port) if port else DEFAULT_PORT
        conn = connect_direct(ip, port)
        if conn:
            chat_session(conn, (ip, port))

    elif choice == "4":
        code = input("Enter Friend 5-digit code: ")
        friend_manager.add_friend(code)

    elif choice == "5":
        friend_manager.show_friends()


if __name__ == "__main__":
    main()
