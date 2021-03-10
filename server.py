import socket
from threading import Thread


class ServerThread(Thread):
    def __init__(self, ip):
        Thread.__init__(self)
        self.ip = ip
        self.threads = []
        self.clients = []

    def run(self):
        TCP_PORT = 9999
        tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpServer.bind((self.ip, TCP_PORT))
        # threads = []

        tcpServer.listen(4)
        while True:
            print("Server is now waiting for connections . . .")
            global conn
            (conn, (ip, port)) = tcpServer.accept()
            self.clients.append(conn)
            newthread = ClientThread(ip, port)
            newthread.start()
            self.threads.append(newthread)
            print("Accepted")
        #
        # for t in threads:
        #     t.join()


class ClientThread(Thread):

    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print("[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self):
        while True:
            # (conn, (self.ip,self.port)) = serverThread.tcpServer.accept()
            global conn
            data = conn.recv(2048)
            print(data.decode("utf-8"))


def main():
    name = socket.gethostname()
    ip = socket.gethostbyname(name)
    ip = "192.168.1.11"
    print(ip)
    server = ServerThread(ip)
    server.start()


if __name__ == "__main__":
    main()
