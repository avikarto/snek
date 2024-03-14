#! /bin/bash
docker stop snek || true
docker container rm snek || true
docker run -itd\
    --name "snek"\
	--network="host"\
    snek:latest
