#!/bin/sh

docker build -t buzzerbuild .
docker run -d -p 1340:1340 -v ~/buzzer:/buzzerlog --cap-add=SYS_ADMIN --cap-add=NET_ADMIN --net=host --restart unless-stopped buzzerbuild
