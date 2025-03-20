This is a secure group chat based socket in python. In this project i'm using AES algorithm in order encrypt
the messages which are being sent over the socket. By this I make sure that clients only will be able to 
decrypt the messages between them and anyone who tries to watch the network transport will not able to see it.

To use the chat, please run the server first and then join as many clients 
as you'd like to by just running the client file on a different console.

Notice: If you're trying to run it please make sure to download additional libraries if needed.
in order to run this line in the client file: 'from Cryptodome.Cipher import AES' 
please write the following in the console: 'pip install pycryptodomex'

Enjoy :)
