import logging
import os
import time
from aiohttp import web
from pathlib import Path
from typing import Callable, Awaitable, Dict, Any
from contextlib import contextmanager

import bluetooth
from bluetooth.ble import GATTRequester


log_file = os.path.join('buzzerlog', 'buzzer.log')
print(log_file)
logging.basicConfig(filename=log_file, filemode='a+', level=logging.DEBUG)
logger = logging.getLogger("buzzer_app")
logger.setLevel(logging.DEBUG)
logger.info("Logger is setup")


with open(str(Path(__file__).parent / "devices.txt")) as f:
    devices = f.readlines()

router = web.RouteTableDef()
_WebHandler = Callable[[web.Request], Awaitable[web.StreamResponse]]



@contextmanager
def connect(device: str):
    req = GATTRequester(device, False, 'hci0')
    req.connect(False, 'random')

    count = 0
    while not req.is_connected():
        if count >= 10 :
            raise ConnectionError('Connection to {} timed out after {} seconds'.
                                  format(device, count))
        time.sleep(1)
        count += 1

    yield req

    if req.is_connected():
        req.disconnect()


@router.get('/')
async def greet_user(request: web.Request) -> Dict[str, Any]:
    logger.info("Home Page")
    print("Home")
    print(f"{logger}")
    logger.info("Opening door")
    for device in devices:
        logger.info(device)

        with connect(device=device) as req:
            print('Connected!')
            out = req.write_by_handle(0x16, b'\x57\x01\x00')
            logger.info(f"Message Sent {out}")
            logger.info('Command execution successful')
    logger.info("END: Opening door")
    return {}


async def init_app() -> web.Application:
    app = web.Application()
    app.add_routes(router)
    return app


if __name__ == '__main__':
    web.run_app(init_app(), port=1340)
