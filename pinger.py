import time
import sys


def main(number):
    while True:
        time.sleep(3)
        print("Waiting for {} connections..".format(number))


if __name__ == '__main__':
    number = sys.argv[1]
    main(number)
