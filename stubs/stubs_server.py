import asyncio
import logging
import sys
from stubs.stubs_api import Api
from stubs.stubs import Stub

stub_data = (
    (1, 'WAY4', 3000),
    (2, 'RSA', 3001),
)


def setup_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(name)s: %(message)s',
        stream=sys.stdout,
    )


class StubServer:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.stubs = {data[0]: Stub(data, self.loop) for data in stub_data}

    def run(self):
        api = Api(self)
        tasks = [self.loop.create_task(stub.start()) for stub in self.stubs.values()]
        tasks.append(api.run())
        self.loop.run_until_complete(asyncio.wait(tasks))
        self.loop.close()

    async def stub_list(self):
        keys = ['id', 'name', 'port', 'running']
        return [{key: value for key, value in stub.__dict__.items() if key in keys}
                for stub in self.stubs.values()]

    async def stub(self, id):
        if id in self.stubs:
            return self.stubs[id].__dict__

    async def start_stub(self, id):
        if id in self.stubs:
            stub = self.stubs[id]
            if not stub.running:
                self.loop.create_task(self.stubs[id].start())
                return f'stub id={id} started'
            else:
                return f'stub id={id} already started'

    async def stop_stub(self, id):
        if id in self.stubs:
            stub = self.stubs[id]
            if stub.running:
                await self.stubs[id].stop()
                return f'stub id={id} stopped'
            else:
                return f'stub id={id} is not started'

    async def start_all(self):
        for id in self.stubs.keys():
            await self.start_stub(id)
        return 'All stubs started'

    async def stop_all(self):
        for id in self.stubs.keys():
            await self.stop_stub(id)
        return 'All stubs stopped'


if __name__ == '__main__':
    setup_logger()
    server = StubServer()
    server.run()
