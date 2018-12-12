
import socket
import sys
import threading
import time

TCP_IP = ''  # All available interfaces
TCP_PORT = 54000
BUFFER_SIZE = 1024


def client_thread(conn, addr):
    now = time.strftime("%H-%M-%S")
    fileName = now + "_" + str(addr[0]) + 'p' + str(addr[1]) + ".txt"
    file = open(fileName, 'w')
    while True:
        data = conn.recv(1024)
        if not data:
            break
        receivedData = data.decode("utf-8")
        receivedData = receivedData[:-1]  # Remove C Sended last caracter
        writeData = time.strftime("%H:%M:%S") + '> ' + receivedData + '\n'
        file.write(writeData)
        conn.sendall(data)  # echo
    print("Closing connection: {} ...".format(str(conn)))
    file.close()
    conn.close()


# Create socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except Exception as msg:
    # print("Could not create socket. Error Code: {}".format(str(msg[1])))
    sys.exit(0)

print("[-] Socket Created")

# Bind socket
try:
    sock.bind((TCP_IP, TCP_PORT))
    print("[-] Socket Bound to port " + str(TCP_PORT))
except Exception as msg:
    print("Bind Failed. Error Code: {} Error: {}".format(str(msg[0]), msg[1]))
    sys.exit()


sock.listen(10)
print("Listening...")


# Loop listening
while True:
    conn, addr = sock.accept()
    print("[-] Connected to " + addr[0] + ":" + str(addr[1]))
    threading.Thread(target=client_thread, args=(conn, addr,)).start()

# Close Socket
sock.close()
