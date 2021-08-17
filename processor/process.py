import asyncio
import json
import numpy
import logging
from common.runner import Runner
# import cv2
from scipy.spatial import KDTree
from webcolors import (
    css3_hex_to_names,
    hex_to_rgb,
)

log = logging.getLogger(__name__)


class Process(Runner):
    names = []
    rgb_values = []

    def __init__(self):
        # a dictionary of all the hex and their respective names in css3
        css3_db = css3_hex_to_names
        for color_hex, color_name in css3_db.items():
            self.names.append(color_name)
            self.rgb_values.append(hex_to_rgb(color_hex))

    def convert_rgb_to_names(self, rgb_tuple) -> str:
        # will count closest color to dictionary colors
        kdt_db = KDTree(self.rgb_values)
        distance, index = kdt_db.query(rgb_tuple)
        return f'{self.names[index]}'

    async def message_handler(self, msg) -> None:
        log.debug("Start handling message")
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

            result_color_name = self.convert_rgb_to_names(average_tuple)

            # send processed file to (writer) third part of solution
            await self.nc.publish("processed", json.dumps({"filename": result['filename'],
                                                           "img": result['img'],
                                                           "color": result_color_name,
                                                           "average": average_tuple}).encode())


if __name__ == '__main__':
    processor = Process()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(processor.run(loop, 'pictures'))
    loop.close()
