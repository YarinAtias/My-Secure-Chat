import socket
import os
from Config import *
import threading

Dict_Of_All_Clients = {}


def Receive_Messages_From_Clients(Socket_Of_Client: socket.socket, Address_Of_Client: tuple) -> None:
    while True:
        try:
            Data_From_Client = Socket_Of_Client.recv(4096)
            if not Data_From_Client:
                raise Exception("Client disconnected")

            print(f"Received encrypted message: {Data_From_Client}\n")
            Send_Messages_To_All_Clients_Broadcast(Socket_Of_Client, Data_From_Client)


        except Exception as e:
            print(f"Disconnected from server, client wanted to quite: {e}")
            Socket_Of_Client.close()
            if Address_Of_Client in Dict_Of_All_Clients:
                del Dict_Of_All_Clients[Address_Of_Client]
            Socket_Of_Client.close()
            break  # Stop the thread


def Send_Messages_To_All_Clients_Broadcast(Socket_Of_The_Sender: socket.socket, Data_Of_Sender) -> None:
    Key = None
    try:
        for Key in Dict_Of_All_Clients.keys():
            Socket_Of_Client = Dict_Of_All_Clients[Key]
            if Socket_Of_The_Sender != Socket_Of_Client:
                Socket_Of_Client.sendall(Data_Of_Sender)

    except Exception as e:
        print(f"It has been a problem sending the messages of the client - {Key}, error - {e} \n")



def Main_Function():
    Listening_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Listening_Socket.bind(Server_Address)
    Listening_Socket.listen(Number_Of_Clients_To_Listen)
    os.system('cls||clear')
    print("Waiting For Clients To connect. All Set Up... \n")
    while True:
        Communicate_Socket, Address_Of_Client = Listening_Socket.accept()
        print(f"{Address_Of_Client} Has Joined The Chat. \n")
        # you do not need to decrypt this message.
        Dict_Of_All_Clients[Address_Of_Client] = Communicate_Socket
        threading.Thread(target=Receive_Messages_From_Clients, args=(Communicate_Socket, Address_Of_Client)).start()


if __name__ == "__main__":
    Main_Function()
