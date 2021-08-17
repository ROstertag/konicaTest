import asyncio
import logging
from nats.aio.client import Client
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

log = logging.getLogger(__name__)


class Runner:
    NATS_ADDRESS = "nats-0.nats.default.svc:4222"

    nc = Client()

    async def message_handler(self, msg):
        pass

    async def run(self, loop, channel) -> None:
        try:
            await self.nc.connect(self.NATS_ADDRESS, loop=loop)

        except ErrConnectionClosed as e:
            log.error("Connection closed prematurely. Error: %s ", e)
        except ErrTimeout as e:
            log.error("Connection Timeout occured. Error: %s ", e)
        except ErrNoServers as e:
            log.error("Problem with connection servers. Error: %s ", e)


        # Simple publisher and async subscriber via coroutine.
        sid = await self.nc.subscribe(channel, cb=self.message_handler)

        while True:
            await asyncio.sleep(1)

        # Remove interest in subscription.
        await nc.unsubscribe(sid)

        # Terminate connection to NATS.
        await nc.close()