import socket
import json
from threading import Thread


class ClientChat:
    HOST = "127.0.0.1"
    PORT = 5002

    def __init__(self, name):
        self.client = socket.socket()
        print(f"Connecting to server {ClientChat.HOST}:{ClientChat.PORT}")
        self.client.connect((ClientChat.HOST, ClientChat.PORT))
        self.client.send(f"{name} enter the chat.".encode())
        self.user_name = name

    def listen_for_messages(self):
        while True:
            try:
                msg = self.client.recv(1024).decode()
                # if self.user_name not in msg:
                print(f"\n{msg}")
            except ConnectionResetError:
                print("Chat ended server is close")
                remove_online_user()
                # self.client.close()
                exit()
                # ClientChat.connect_users.remove(self.user_name)
                break

    def start_client(self):
        t = Thread(target=self.listen_for_messages)
        t.daemon = True
        t.start()

        while True:
            msg_to_send = input()

            # to stop sending messages

            if msg_to_send.lower() == "q":
                # to fix server side error on exit
                remove_online_user()
                self.client.send(f"{self.user_name} has left the chat.".encode())
                # self.client.close()
                exit()
                # ClientChat.connect_users.remove(self.user_name)
                break

            msg_to_send = f"{self.user_name} - {msg_to_send}"
            self.client.send(msg_to_send.encode())



    @staticmethod
    def check_for_user_name_duplicate():
        name_ = input("Enter nickname: ").lower()
        online = open_online_users()
        if name_ in online:
            while True:
                name_ = input("That nickname is already taken\nEnter nickname: ").lower()
                if name_ not in online:
                    online.append(name_)
                    save_online_users(online)
                    break
        else:
            online.append(name_)
            save_online_users(online)
        return name_


def open_online_users():
    with open("online_users.json", "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data


def save_online_users(data):
    with open("online_users.json", "w", encoding='utf-8') as json_file:
        json.dump(data, json_file)


def remove_online_user():
    online = open_online_users()
    online.remove(cc.user_name)
    save_online_users(online)


cc = ClientChat(ClientChat.check_for_user_name_duplicate())
cc.start_client()
