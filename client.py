import socket
import threading
import sys
import time


def listen_server_words(s):
    while True:
        try:
            s.connect(('127.0.0.1', 50000))
        except ConnectionRefusedError:
            print("Trying co connect to server {} {} ...".format('127.0.0.1', 50000))
            time.sleep(2)
        else:
            print("Connection with {} {} was established".format('127.0.0.1', 50000))
            break
    print("To finish connection print: quit")
    while True:
        try:
            data = s.recv(1024)
            if data:
                data = data.decode('utf-8')
                print("{} {}: {}".format('127.0.0.1', 50000, data))
        except ConnectionResetError:
            print("Session was finished by remote host")
            break


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    th = threading.Thread(target=listen_server_words, args=(s,), daemon=True)
    th.start()
    while True:
        word = input(">>")
        try:
            s.sendall(word.encode('utf-8'))
            if word == "quit":
                try:
                    s.close()
                except ConnectionAbortedError:
                    pass
                finally:
                    print("Session was finished by us")
                    sys.exit(100)
        except ConnectionResetError:
            print("The other side stopped connection earlier")
            print("Please close the program")
        except OSError:
            pass
