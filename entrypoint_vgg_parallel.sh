#!/bin/bash

export ID=$1
export ADDRESS=http://0.0.0.0:6666
export RESNET_PARALLEL=True

echo "ID: $1"
exec gunicorn -k flask_sockets.worker grid_node_modified:app \
"$@"
