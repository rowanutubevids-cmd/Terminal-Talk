import socket
import threading


def start_lan_listener(port, chat_callback):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))
    server.listen(1)

    print(f"Listening on port {port}...")

    conn, addr = server.accept()
    chat_callback(conn, addr)


def connect_direct(ip, port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        return client
    except Exception as e:
        print("Connection failed:", e)
        return None
