#!/bin/bash
export ID=bob
export ADDRESS=http://0.0.0.0:6667

exec gunicorn -k flask_sockets.worker grid_node:app \
"$@"