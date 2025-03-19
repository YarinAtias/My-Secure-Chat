import socket
import threading
from Cryptodome.Cipher import AES
import pickle

key = b"This_key_for_AES"

def EncryptText(Text: str):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(Text.encode())
    nonce = cipher.nonce
    return nonce, tag, ciphertext
    # Returns 3 variables which crucial for the encryption and the decryption of AES algorithm


def DecryptText(nonce, tag, CipherText):
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(CipherText, tag)
    return data.decode()


def SendMessageToServer(MySocket: socket.socket):
    global is_socket_active
    while is_socket_active:
        print("You: ", end="")
        data = input().strip()
        if data.lower() == "q":  # If the user choose to end chatting
            print("Quitting...")
            is_socket_active = False
            MySocket.close()
            break
        elif len(data) == 0:  # If the input is empty
            pass
        else:  # Send a message to the server
            ClientInput = f"{UserName}: " + data.capitalize()
            nonce, tag, EncryptedInput = EncryptText(ClientInput)
            try:
                DataList = [nonce, tag, EncryptedInput]  # Sends a list of the 3 crucial variables for the AES to the server
                DataListInBytes = pickle.dumps(DataList)
                MySocket.sendall(DataListInBytes)
            except (BrokenPipeError, ConnectionAbortedError):
                break


def ReceiveMessagesFromOthers(MySocket: socket.socket):
    global is_socket_active
    while is_socket_active:
        try:
            received_data = MySocket.recv(4096)
            DataList = pickle.loads(received_data)
            nonce, tag, Message = DataList[0], DataList[1], DataList[2]
            DecryptedMessage = DecryptText(nonce, tag, Message)
            print("\r" + DecryptedMessage, flush=True)
            print("You: ", end="", flush=True)
        except (ConnectionAbortedError, ConnectionResetError):
            break
    is_socket_active = False



def main():
    global UserName
    global is_socket_active
    print("Notice: You can enter Q/q in order to end chatting")
    UserName = input("Enter your nickname for chatting: ").capitalize()
    Client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ClientIP = "127.0.0.1"
    ClientPort = 8090
    Client_socket.connect((ClientIP, ClientPort))
    print("You can start chatting 😊\n")
    is_socket_active = True
    threading.Thread(target=ReceiveMessagesFromOthers, args=(Client_socket,)).start()  # Receive Messages Thread
    threading.Thread(target=SendMessageToServer, args=(Client_socket,)).start()  # Send Messages Thread


if __name__ == "__main__":
    main()