from saqws import SAQPubServer
import aiohttp
import aiohttp.web
import asyncio
import datetime
import logging


logger = logging.getLogger(__name__)


async def generate_data(pub_server):
    while True:
        start_lap = datetime.datetime.now()
        total_dur = 0
        for lap in range(100):
            await asyncio.sleep(1)
            end_lap = datetime.datetime.now()
            duration = (end_lap - start_lap)
            total_dur += duration.seconds
            msg = {'lap': lap+1, 'time': duration.seconds, 'total': total_dur}
            print(msg)
            pub_server.append(msg)
            start_lap = end_lap
        pub_server.start_new_session()


async def app_entrypoint():
    app = aiohttp.web.Application()

    # attach the SAQPubServer
    pub_server = SAQPubServer(app, '/saqws')

    loop = asyncio.get_event_loop()
    loop.create_task(generate_data(pub_server))
    return app


async def main(host, port):
    app = await app_entrypoint()
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner=runner, host=host, port=port, ssl_context=None)
    await site.start()

    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    localhost = 'localhost'
    localport = 9876

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(localhost, localport))
