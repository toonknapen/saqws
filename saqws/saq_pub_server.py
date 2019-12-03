import aiohttp, aiohttp.web
import asyncio
from .sessionawareasynclist import SessionAwareAsyncList
import logging

logger = logging.getLogger(__name__)


class SAQPubServer(object):
    """

    """
    def __init__(self, app, path):
        self._saal = SessionAwareAsyncList()
        app.router.add_routes([aiohttp.web.get(path, self._sub_connection_handler)])

    def append(self, msg):
        try:
            logger.debug(f'append #{self._saal.size()}: {msg} ')
            self._saal.append(msg)
        except:
            logger.exception('Something went wrong while sending msg-buffer')

    def start_new_session(self):
        self._saal.start_new_session()

    def stop(self):
        self._saal.stop()

    async def _sub_connection_handler(self, request):
        """
        Handler function called for every sub that connects on the websocket

        :param request:
        :return:
        """
        session = self._saal.session()
        num_send = 0
        logger.info(f"Sub connection, backlog-depth:{self._saal.size()}")

        ws = aiohttp.web.WebSocketResponse()
        await ws.prepare(request)

        # On initial connect, send the whole backlog at once

        try:
            while session >= 0:
                while True:  # handle the current session
                    backlog = await self._saal.wait(session, num_send)
                    if backlog is None:
                        break  # another session must have started or this was the last session
                    for i in backlog:
                        logger.debug(f"Sending (session #{session}):{i}")
                        await ws.send_json(i)
                        num_send += 1

                session = self._saal.session()  # get the new session that has started
                num_send = 0
                await ws.send_json(None)
        except asyncio.CancelledError:
            logger.info("WS Canceled")
        except:
            logger.exception('something went wrong')

        logger.warning('Pub closing WS')
        await ws.close()
        return ws
