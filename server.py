import socket
import subprocess
import threading
import sys


def listen_client_words(conn, addr):
    while True:
        try:
            data = conn.recv(1024)
            if data:
                data = data.decode('utf-8')
                print("{} {}:  {}".format(*addr, data))
        except ConnectionResetError:
            print("Session was finished by remote host")
            break


def server_run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        ip, port = '127.0.0.1', 50000
        s.bind((ip, port))
        s.listen(1)
        pinger = subprocess.Popen(["python", "pinger.py", "1"])
        conn, addr = s.accept()
        pinger.kill()
        print("Connection with {} {} was established".format(*addr))
        print("To finish connection print: quit")
        th = threading.Thread(target=listen_client_words, args=(conn, addr,), daemon=True)
        th.start()
        while True:
            word = input(">>")
            try:
                conn.sendall(word.encode('utf-8'))
                if word == "quit":
                    try:
                        conn.close()
                        s.close()
                    except ConnectionAbortedError:
                        pass
                    finally:
                        print("Session was finished by us")
                        sys.exit(100)
            except ConnectionResetError:
                print("The other side stopped connection earlier")
                print("Please close the program")


if __name__ == '__main__':
    server_run()

