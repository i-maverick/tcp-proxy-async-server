import asyncio
import logging
import sys
import time

SERVER_ADDRESS = ('127.0.0.1', 2222)


async def stub_server(loop):
    await asyncio.start_server(stub_handler, *SERVER_ADDRESS, loop=loop)


async def stub_handler(reader, writer):
    address = writer.get_extra_info('peername')
    log = logging.getLogger('{}_{}'.format(*address))
    log.debug('connection accepted')

    while True:
        data = await reader.read(1024)
        if data:
            log.debug('received {!r}'.format(data))
            time.sleep(1)
            writer.write(data)
            await writer.drain()
            log.debug('sent {!r}'.format(data))
        else:
            log.debug('connection closing')
            writer.close()
            return


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(name)s: %(message)s',
        stream=sys.stdout,
    )

    event_loop = asyncio.get_event_loop()
    server = event_loop.run_until_complete(stub_server(event_loop))

    print('starting up on {}:{}'.format(*SERVER_ADDRESS))

    try:
        event_loop.run_forever()
    finally:
        server.close()
        event_loop.run_until_complete(server.wait_closed())
        event_loop.close()


if __name__ == '__main__':
    main()
