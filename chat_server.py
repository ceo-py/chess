import socket
from threading import Thread


class ChatServer:
    HOST = "0.0.0.0"
    PORT = 5002
    users_information = {}

    def __init__(self):
        self.server = socket.socket()  # create tcp socket
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # the port become reusable
        self.server.bind((ChatServer.HOST, ChatServer.PORT))  # put that info into the server
        self.users_information = {}
        self.server.listen()
        print(f"Listening as {ChatServer.HOST}: {ChatServer.PORT}")

    def start_server(self):
        while True:
            user_socket, user_address = self.server.accept()
            print(f"{user_address} connected.")
            self.users_information[user_socket] = user_socket
            t = Thread(target=self.listen_for_messages, args=(user_socket,))
            # t.daemon = True
            t.start()

    def stop_server(self):
        for user in self.users_information.values():
            user.close()

        self.server.close()

    def listen_for_messages(self, user):

        while True:
            try:
                # checking for msg
                msg = user.recv(1024).decode()

            except Exception:
                # try:
                    # remove the user if he dc
                    print("User left the chat")
                    del self.users_information[user]
                    user.close()
                # except:
                #     print("Done")
                #     break


            # going over user and send the msg
            for user_msg in self.users_information.values():
                user_msg.send(msg.encode())


cs = ChatServer()
cs.start_server()
