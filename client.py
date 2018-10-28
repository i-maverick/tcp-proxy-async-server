import socket
import time
import random

READ_BUFFER = 4096

HSM_PROXY_HOST = '127.0.0.1'
HSM_PROXY_PORT = 3000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HSM_PROXY_HOST, HSM_PROXY_PORT)
sock.connect(server_address)
print('connecting to {0}:{1}'.format(*server_address))

client_id = random.randint(0, 32767)  # add unique identifier of the client

for i in range(10):
    text = 'This is the message {}'.format(i)
    message = '{0} {1}'.format(client_id, text)
    print('sending "{0}"'.format(message))
    sock.sendall(bytes(message, encoding='utf-8'))

    data = sock.recv(READ_BUFFER)
    print('received "{0}"'.format(data.decode("utf-8")))

    # time.sleep(random.randint(0, 10))

# while True:
#     data = sock.recv(READ_BUFFER)
#     if data:
#         print(data)

print('closing socket')
sock.close()
# time.sleep(10)
