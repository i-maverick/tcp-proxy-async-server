import json
from aiohttp import web

HOST = '127.0.0.1'
PORT = 8000


class Api:
    def __init__(self, server):
        self.server = server

    def setup_routes(self, app):
        app.router.add_get('/stubs', self.stub_list)
        app.router.add_get('/stubs/{id}/', self.get_stub)
        app.router.add_get('/stubs/{id}/start', self.start_stub)
        app.router.add_get('/stubs/{id}/stop', self.stop_stub)
        app.router.add_get('/stubs/start_all', self.start_all)
        app.router.add_get('/stubs/stop_all', self.stop_all)

    def run(self):
        app = web.Application()
        self.setup_routes(app)
        web.run_app(app, host=HOST, port=PORT)

    async def stub_list(self, request):
        lst = await self.server.stub_list()
        return self.response({'stubs': lst})

    async def get_stub(self, request):
        id = int(request.match_info.get('id'))
        ret = await self.server.get_stub(id)
        if ret:
            return self.response(ret)

    async def start_stub(self, request):
        id = int(request.match_info.get('id'))
        ret = await self.server.start_stub(id)
        if ret:
            return self.response({'result': ret})

    async def stop_stub(self, request):
        id = int(request.match_info.get('id'))
        ret = await self.server.stop_stub(id)
        if ret:
            return self.response({'result': ret})

    async def start_all(self, request):
        ret = await self.server.start_all()
        return self.response({'result': ret})

    async def stop_all(self, request):
        ret = await self.server.stop_all()
        return self.response({'result': ret})

    @staticmethod
    def response(obj):
        return web.Response(status=200, body=json.dumps(obj))

    @staticmethod
    def error(msg):
        print(f'Error: {msg}')
        return web.Response(status=400, body=msg)
