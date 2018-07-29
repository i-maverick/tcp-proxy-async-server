import asyncio
import logging
import sys

HOST = '127.0.0.1'
READ_BUFFER = 2048

stub_data = (
    (1, 'WAY4', 3000),
    (2, 'E-PG', 3001),
    (3, 'E-IB', 3002),
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

        self.reader = None
        self.writer = None

        self.running = False

        self.log = logging.getLogger(f'{name}_{port}')

    def close(self, err):
        print(f'Closing connection: {err}')
        if self.writer:
            self.writer.close()
        self.running = False

    async def start(self):
        self.log.debug(f'Starting stub {self.name}')
        try:
            self.reader, self.writer = await asyncio.open_connection(
                host=HOST, port=self.port, loop=self.loop)
            self.running = True
            self.log.debug(f'Stub connected to port {self.port}')
        except (asyncio.TimeoutError, ConnectionRefusedError) as err:
            self.close(err)
            return

        while self.running:
            data = await self.reader.read(READ_BUFFER)
            if not data:
                self.close('no data')
                return

            self.log.debug('received {!r}'.format(data))

            response = await self.prepare_response(data)

            self.writer.write(response)
            await self.writer.drain()
            self.log.debug('sent {!r}'.format(response))

    @staticmethod
    async def prepare_response(data):
        await asyncio.sleep(0.5)
        return data

    def stop(self):
        self.running = False


def create_stubs():
    loop = asyncio.get_event_loop()
    stubs = [Stub(s[1], s[2], loop) for s in stub_data]
    tasks = [loop.create_task(stub.start()) for stub in stubs]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == '__main__':
    setup_logger()
    create_stubs()
