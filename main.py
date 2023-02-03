import json
import socket
import jwt
import time
from database.db import register, login, get_questions, question_category, get_user_id, update_user_answer



def createToken(username):
    timestamp = str(int(time.time()))
    encoded_jwt = jwt.encode({"username": username, "time": timestamp}, "hjfkdasiubvdndsf", algorithm="HS256")
    return encoded_jwt


def server_program():
    host = socket.gethostname()  # get the hostname
    port = 5000  # initiate port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(5)  # configure how many client the server can listen simultaneously

    while True:
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        try:
            data = conn.recv(1024)  # receive data stream. it won't accept data packet greater than 1024 bytes
            json_data = data.decode()
            data = json.loads(json_data)
            print("Received:", data)
            if data["action_type"] == "login":
                if login(data["username"], data["password"]):
                    answer = {"answer": True, "token": createToken(data["username"])}
                else:
                    answer = {"answer": False}
            elif data["action_type"] == "register":
                if register(data["username"], data["password"]):
                    answer = {"answer": True, "token": createToken(data["username"])}
                else:
                    answer = {"answer": False}
            elif data["action_type"] == "category":
                answer = question_category()
            elif data["action_type"] == "questions":
                decoded_token = jwt.decode(data["token"], "hjfkdasiubvdndsf", algorithms=['HS256'])
                user_id = get_user_id(decoded_token["username"])
                print(data["category"])
                answer = get_questions(user_id, data["category"])
            elif data["action_type"] == "user_answers":
                user_id = get_user_id(decoded_token["username"])
                update_user_answer(user_id, data["question_id"], data["date"])
            else:
                answer = {"answer": False}
            print("Sending: ", str(answer))
            conn.send(json.dumps(answer).encode())  # send data to the client
        finally:
            print("Close connection from: " + str(address))
            conn.close()  # close the connection


if __name__ == '__main__':
    server_program()