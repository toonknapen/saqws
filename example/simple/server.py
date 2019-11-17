from saqws import SAQPubServer
import asyncio
import datetime
import logging


logger = logging.getLogger(__name__)
host = 'localhost'
port = 9876

async def main():
    pub_server = SAQPubServer()
    await pub_server.launch(host=host, port=port)

    while True:
        start_lap = datetime.datetime.now()
        total_dur = 0
        for lap in range(100):
            await asyncio.sleep(1)
            end_lap = datetime.datetime.now()
            duration = (end_lap - start_lap)
            total_dur += duration.seconds
            msg = {'lap': lap+1, 'time': duration.seconds, 'total': total_dur}
            logger.warning(msg)
            pub_server.append(msg)
            start_lap = end_lap
        pub_server.start_new_session()


if __name__ == '__main__':
    asyncio.run(main())