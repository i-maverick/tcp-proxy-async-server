import asyncio
import logging


HOST = '127.0.0.1'
READ_BUFFER = 2048


class Stub:
    def __init__(self, data, loop):
        self.id, self.name, self.port = data
        self.loop = loop

        self.reader = None
        self.writer = None

        self.running = False

        self.log = logging.getLogger(f'{self.name}_{self.port}')

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

    async def stop(self):
        self.running = False
