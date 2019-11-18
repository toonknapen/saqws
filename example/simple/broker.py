from saqws import SAQSubClient
import asyncio
import logging


logger = logging.getLogger(__name__)
host = 'localhost'
port = 9876

async def main():
    queue = asyncio.Queue()
    sub_client = SAQSubClient(data_buffer=queue, formatter=lambda x: x)
    sub_client.connect(host=host, port=port, path='/saqws')

    while True:
        msg = await queue.get()
        print(msg)

if __name__ == '__main__':
    asyncio.run(main())