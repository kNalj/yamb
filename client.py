from threading import Thread
import socket


class ClientThread(Thread):
    def __init__(self, ip):
        super().__init__()

        self.ip = ip
        self.port = 9999

    def run(self):
        BUFFER_SIZE = 2000
        global tcpClientA
        tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpClientA.connect((self.ip, self.port))

        while True:
            data = tcpClientA.recv(BUFFER_SIZE)
            print(data.decode("utf-8"))
        # tcpClientA.close()


def main():
    client = ClientThread("192.168.1.11")
    client.start()


if __name__ == "__main__":
    main()
