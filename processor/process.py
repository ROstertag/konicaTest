import asyncio
import json
import numpy
# import cv2
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
from scipy.spatial import KDTree
from webcolors import (
    css3_hex_to_names,
    hex_to_rgb,
)


def convert_rgb_to_names(rgb_tuple):
    # a dictionary of all the hex and their respective names in css3
    css3_db = css3_hex_to_names
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))

    # will count closest color
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return f'{names[index]}'


async def run(loop):
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
        # test for proper input
        if 'img' in result:
            img = numpy.array(result['img'])

            # counts average color of image
            average = img.mean(axis=0).mean(axis=0)

            # I will comment this but probably would be better to count dominant color
            # we use average because it was defined in task
            ''' pixels = numpy.float32(img.reshape(-1, 3))

            n_colors = 5
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
            flags = cv2.KMEANS_RANDOM_CENTERS

            _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
            _, counts = numpy.unique(labels, return_counts=True)

            dominant = palette[numpy.argmax(counts)]
            '''
            average_tuple = (int(average[0]), int(average[1]), int(average[2]))

            result_color_name = convert_rgb_to_names(average_tuple)

            # send processed file to (writer) third part of solution
            await nc.publish("processed", json.dumps({"filename": result['filename'],
                                                      "img": result['img'],
                                                      "color": result_color_name,
                                                      "average": (int(average[0]),
                                                                  int(average[1]),
                                                                  int(average[2]))}.encode()))

    # Simple publisher and async subscriber via coroutine.
    sid = await nc.subscribe("pictures", cb=message_handler)

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
