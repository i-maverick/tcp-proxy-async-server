import asyncio
import logging
import sys

HOST = '127.0.0.1'

stubs = (
    (1, 'ATM', 4001),
    (2, 'E-PG', 4002),
    (3, 'E-IB', 4003),
)


def setup_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(name)s: %(message)s',
        stream=sys.stdout,
    )


class Stub:
    def __init__(self, name, port, loop):
        self.name = name
        self.port = port
        self.loop = loop

        self.log = logging.getLogger('{}_{}'.format(self.name, port))

    async def start(self):
        await asyncio.start_server(self.handler, HOST, self.port, loop=self.loop)
        self.log.debug('starting up')

    async def handler(self, reader, writer):
        self.log.debug('connection accepted')
        while True:
            data = await reader.read(1024)
            if data:
                self.log.debug('received {!r}'.format(data))

                response = self.prepare_response(data)

                writer.write(response)
                await writer.drain()
                self.log.debug('sent {!r}'.format(response))
            else:
                self.log.debug('connection closing')
                writer.close()
                return

    async def prepare_response(self, data):
        return data


class TcpStub(Stub):
    async def prepare_response(self, data):
        response = bytes(self.name, encoding='utf-8') + data
        return response


class MqStub(Stub):
    async def prepare_response(self, data):
        response = bytes(self.name, encoding='utf-8') + data
        return response


async def create_stubs(loop):
    for s in stubs:
        stub = TcpStub(s[1], s[2], loop)
        await stub.start()


def main():
    setup_logger()

    event_loop = asyncio.get_event_loop()
    server = event_loop.run_until_complete(create_stubs(event_loop))

    try:
        event_loop.run_forever()
    finally:
        server.close()
        event_loop.run_until_complete(server.wait_closed())
        event_loop.close()


if __name__ == '__main__':
    main()
