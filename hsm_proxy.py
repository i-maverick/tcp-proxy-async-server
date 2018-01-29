import asyncio

READ_BUFFER = 4096
HSM_HOST = '127.0.0.1'
HSM_PORT = 3333

HSM_PROXY_HOST = '127.0.0.1'
HSM_PROXY_PORT = 2222


class HSMProxyServer:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def client(self, loop):
        hsm_reader, hsm_writer = await asyncio.open_connection(HSM_HOST, HSM_PORT, loop=loop)

        while True:
            try:
                item = await self.queue.get()
                writer, message = item
                print('Send: %r' % message)
                hsm_writer.write(message)

                data = await hsm_reader.read(READ_BUFFER)
                response = data.decode()
                print('Received: %r' % response)

                writer.write(data)
                await writer.drain()
            except ConnectionResetError as ex:
                print(ex)
                writer.close()

        # print('Close the socket')
        # writer.close()

    async def server(self, reader, writer):
        while True:
            try:
                data = await reader.read(READ_BUFFER)
            except ConnectionResetError as ex:
                print(ex)
                writer.close()
                break

            if not data:
                writer.close()
                break

            addr = writer.get_extra_info('peername')
            print("Received %r from %r" % (data.decode(), addr))

            self.queue.put_nowait((writer, data))


hsm_proxy = HSMProxyServer()
loop = asyncio.get_event_loop()
coro = asyncio.start_server(hsm_proxy.server, HSM_PROXY_HOST, HSM_PROXY_PORT, loop=loop)
server = loop.run_until_complete(asyncio.gather(hsm_proxy.client(loop), coro))

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
