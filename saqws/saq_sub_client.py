import logging
import aiohttp
import aiohttp.client_exceptions
import asyncio
import typing

logger = logging.getLogger(__name__)


class SAQSubClient:
    """
    Queue-subscriber putting messages from publisher into provided data-buffer

    A 'None' in the queue signals a new session that is started
    """
    def __init__(self, data_buffer: asyncio.Queue, formatter: typing.Callable[[str], dict]):
        self._data_buffer = data_buffer
        self._formatter = formatter
        self._try_to_connect = True
        self._reconnect_interval = 5

    def connect(self, scheme, host, port, path):
        assert path[0] == '/'

        loop = asyncio.get_event_loop()
        self._task = loop.create_task(self._start(scheme=scheme, host=host, port=port, path=path))

    async def wait(self):
        await self._task

    def done(self):
        return self._task.done()

    async def _start(self, scheme: str, host: str, port: int, path: str):
        url = f"{scheme}://{host}{path}" if port is None else f"{scheme}://{host}:{port}{path}"
        while self._try_to_connect:
            try:
                async with aiohttp.ClientSession() as session:
                    logger.debug('Sub started new session')
                    async with session.ws_connect(url=url) as ws:
                        logger.debug('Sub connected')
                        async for msg in ws:
                            logger.debug(f'Sub received {msg}')
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                formatted_msg = self._formatter(msg.data)
                                self._data_buffer.put_nowait(formatted_msg)
                            else:
                                logger.info(f'inter-websocket received:{msg}')
                logger.info(f"ws closed")

            except aiohttp.client_exceptions.ClientConnectionError:
                logger.error(f"Failed to connect to saqws server at {url}")
            except:
                logger.exception('QSub listener encountered an exception')
            logger.warning(f"Retrying to connect to server in {self._reconnect_interval}s.")
            await asyncio.sleep(self._reconnect_interval)
