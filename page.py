import logging
import os
import time
from aiohttp import web
from pathlib import Path
from typing import Callable, Awaitable, Dict, Any
from gattlib import GATTRequester


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


@router.get('/')
async def greet_user(request: web.Request) -> Dict[str, Any]:
    logger.info("Home Page")
    print("Home")
    print(f"{logger}")
    logger.info("Opening door")
    for device in devices:
        logger.info(device)
        req = GATTRequester(device, False)
        logger.info("Pre-Connect")
        req.connect(False, 'random')
        n_remaining = 10
        while n_remaining > 0:
            logger.info("Pre-sleep")
            time.sleep(1)
            if req.is_connected():
                req.write_by_handle(0x16, b'\x57\x01\x00')
                logger.info("Message Sent")
                req.disconnect()
                break
            n_remaining -= 1
    logger.info('Command execution successful')
    return {}


async def init_app() -> web.Application:
    app = web.Application()
    app.add_routes(router)
    return app


if __name__ == '__main__':
    web.run_app(init_app(), port=1340)
