import asyncio
import time

READ_BUFFER = 4096
HOST = '127.0.0.1'
PORT = 2222


async def server():
    # Start a socket server, call back for each client connected.
    # The client_connected_handler coroutine will be automatically converted to a Task
    await asyncio.start_server(client_handler, HOST, PORT)


async def client_handler(client_reader, client_writer):
    print("Connection received!")
    while True:
        data = await client_reader.read(READ_BUFFER)
        if not data:
            break
        s = data.decode("utf-8")
        print(s)
        response = '{0} {1}'.format(s.split(' ')[0], 'Ok')
        time.sleep(1)
        client_writer.write(bytes(response, encoding='utf-8'))


loop = asyncio.get_event_loop()
loop.run_until_complete(server())
try:
    loop.run_forever()
finally:
    loop.close()
