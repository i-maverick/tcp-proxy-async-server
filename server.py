import asyncio

READ_BUFFER = 4096

HOST = '127.0.0.1'
PORT = 3000


async def server(host, port):
    await asyncio.start_server(client_handler, host, port)
    print('HSM Server started...')


async def client_handler(client_reader, client_writer):
    print("Connection received!")
    try:
        while True:
            data = await client_reader.read(READ_BUFFER)
            if not data:
                break
            s = data.decode("utf-8")
            print(s)
            response = '{0} {1}'.format(s.split(' ')[0], 'Ok')
            client_writer.write(bytes(response, encoding='utf-8'))
    except ConnectionResetError as er:
        print(er)

loop = asyncio.get_event_loop()
loop.run_until_complete(server(HOST, PORT))
try:
    loop.run_forever()
finally:
    loop.close()
