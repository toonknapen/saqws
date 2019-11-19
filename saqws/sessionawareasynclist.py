from typing import Optional, List
import asyncio

class SessionAwareAsyncList:

    def __init__(self):
        self._event = asyncio.Event()
        self._session = 0
        self._list = []

    def append(self, e) -> None:
        """
        Add data to the given session

        :param e:
        :return: None
        """
        self._list.append(e)
        self._trigger_waiters()

    def start_new_session(self) -> None:
        """
        Start new session

        :return: None
        """
        self._list.clear()
        self._session += 1
        self._trigger_waiters()

    def stop(self) -> None:
        """
        Signal to waiters that no new sessions will be coming

        :return: None
        """
        self._list.clear()
        self._session = -1
        self._trigger_waiters()

    def session(self) -> int:
        return self._session

    def size(self) -> int:
        return len(self._list)

    async def wait(self, session: int, as_of) -> Optional[List]:
        """
        Wait for item 'as_of' and later of the given session

        :param session:
        :param as_of:
        :return:
        """
        if session == self._session:

            # if the subscriber is behind, let him catch up immediately
            if as_of < len(self._list):
                return self._list[as_of:]

            # if the subscriber has catched up, just wait for the signal
            await self._event.wait()

            # if the subscriber is signaled about an update,
            # first check if still the same session
            if session == self._session:
                if as_of < len(self._list):
                    return self._list[as_of:]
                else:
                    return []

        # signal that in the meantime another session has started
        return None

    def _trigger_waiters(self) -> None:
        self._event.set()
        self._event.clear()

