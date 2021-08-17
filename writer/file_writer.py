import asyncio
import json
import numpy
import os
import cv2
import logging
from common.runner import Runner

log = logging.getLogger(__name__)


class Writer(Runner):
    path = os.getcwd()

    async def message_handler(self, msg) -> None:
        print("Start handling message")
        data = msg.data.decode()
        result = json.loads(data)
        if 'img' in result:
            # file Upload folder
            upload_folder = os.path.join(self.path, str(result['color']))

            # Make directory if specific folder does not exist
            if not os.path.isdir(upload_folder):
                os.mkdir(upload_folder)

            # Change the current directory
            # to specified directory
            os.chdir(upload_folder)

            # Using cv2.imwrite() method
            # Saving the image
            cv2.imwrite(str(result['filename']), numpy.array(result['img']))

            # we can send info about stored files into frontend from here /optional
            # await nc.publish("stored", json.dumps({"filename": result['filename'],
            #                                       "color": result['color']}).encode())


if __name__ == '__main__':
    writer = Writer()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(writer.run(loop, 'processed'))
    loop.close()
