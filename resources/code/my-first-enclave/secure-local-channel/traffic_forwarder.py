import socket
import sys
import threading
import time

def server(local_ip, local_port, remote_cid, remote_port):
    while True:
        try:
            print(f"[DEBUG] Starting server on {local_ip}:{local_port}")
            dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dock_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            dock_socket.bind((local_ip, local_port))
            dock_socket.listen(5)
            print(f"[DEBUG] Server listening on {local_ip}:{local_port}")

            while True:
                print("[DEBUG] Waiting for client connection...")
                client_socket, client_addr = dock_socket.accept()
                print(f"[DEBUG] Client connected from {client_addr}")

                print(f"[DEBUG] Connecting to enclave at {remote_cid}:{remote_port}")
                server_socket = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
                server_socket.connect((remote_cid, remote_port))
                print("[DEBUG] Connected to enclave")

                threading.Thread(target=forward, args=(client_socket, server_socket, "client->enclave"), daemon=True).start()
                threading.Thread(target=forward, args=(server_socket, client_socket, "enclave->client"), daemon=True).start()

        except Exception as e:
            print(f"[ERROR] Server error: {e}")
            time.sleep(1)  # prevent rapid restart loops
        finally:
            try:
                dock_socket.close()
            except:
                pass

def forward(source, destination, direction):
    try:
        while True:
            data = source.recv(4096)
            if not data:
                print(f"[DEBUG] {direction} - Connection closed")
                break
            print(f"[DEBUG] {direction} - Forwarding {len(data)} bytes")
            destination.sendall(data)
    except Exception as e:
        print(f"[ERROR] {direction} - Forward error: {e}")
    finally:
        try:
            source.shutdown(socket.SHUT_RD)
        except:
            pass
        try:
            destination.shutdown(socket.SHUT_WR)
        except:
            pass
        source.close()
        destination.close()

def main(args):
    if len(args) != 4:
        print(f"Usage: {args[0]} <local_ip> <local_port> <remote_cid> <remote_port>")
        sys.exit(1)

    local_ip = str(args[0])
    local_port = int(args[1])
    remote_cid = int(args[2])
    remote_port = int(args[3])

    print(f"[DEBUG] Configuration: local={local_ip}:{local_port}, remote={remote_cid}:{remote_port}")
    threading.Thread(target=server, args=(local_ip, local_port, remote_cid, remote_port), daemon=True).start()

    print(f"[DEBUG] Traffic forwarder started on {local_ip}:{local_port} -> {remote_cid}:{remote_port}")
    while True:
        time.sleep(60)
        print("[DEBUG] Traffic forwarder heartbeat")

if __name__ == '__main__':
    main(sys.argv[1:])
