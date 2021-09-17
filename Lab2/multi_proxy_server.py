#!/usr/bin/env python3
import socket, sys
from multiprocessing import Process

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Host name could not be resolved. Exiting.')
        sys.exit()

    print (f'IP address of {host} is {remote_ip}')
    return remote_ip

def handle_proxy_server(addr, conn, proxy_end):
    print("Connected by", addr)
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending received data {send_full_data} to google")
    conn.sendall(send_full_data)

    conn.shutdown(socket.SHUT_RDWR)
    data = proxy_end.recv(BUFFER_SIZE)
    print(f"Sending received data {data} to client")
    conn.send(data)
    conn.close()

def main():
    host = 'www.google.com'
    port = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))

        proxy_start.listen(2)
        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(host)
                proxy_end.connect((remote_ip, port))

                p = Process(target=handle_proxy_server, args=(addr, conn, proxy_end))
                p.daemon = True
                p.start()
                print("Child process started", p)
            conn.close()

if __name__ == "__main__":
    main()