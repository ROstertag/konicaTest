import asyncio
import json
import numpy
import os
import cv2
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers


async def run(loop):
    # Get current path
    path = os.getcwd()

    nc = NATS()

    try:
        await nc.connect("nats-0.nats.default.svc:4222", loop=loop)

    except ErrConnectionClosed as e:
        print("Connection closed prematurely. Error: %s ", e)
    except ErrTimeout as e:
        print("Connection Timeout occured. Error: %s ", e)
    except ErrNoServers as e:
        print("Problem with connection servers. Error: %s ", e)

    async def message_handler(msg):
        print("Start handling message")
        data = msg.data.decode()
        result = json.loads(data)
        if 'img' in result:
            # file Upload folder
            upload_folder = os.path.join(path, str(result['color']))

            # Make directory if specific folder does not exist
            if not os.path.isdir(upload_folder):
                os.mkdir(upload_folder)

            # Change the current directory
            # to specified directory
            os.chdir(upload_folder)

            # Using cv2.imwrite() method
            # Saving the image
            cv2.imwrite(str(result['filename']), numpy.array(result['img']))

            # we will send info about stored files into frontend
            await nc.publish("stored", json.dumps({"filename": result['filename'],
                                                   "color": result['color']}).encode())

    # Simple publisher and async subscriber via coroutine.
    sid = await nc.subscribe("processed", cb=message_handler)
    print("after subscribe")

    while True:
        await asyncio.sleep(1)

    # Remove interest in subscription.
    await nc.unsubscribe(sid)

    # Terminate connection to NATS.
    await nc.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()
