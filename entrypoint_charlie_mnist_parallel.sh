#!/bin/bash
export ID=charlie
export ADDRESS=http://0.0.0.0:6668
export MNIST_PARALLEL=True

exec gunicorn -k flask_sockets.worker grid_node_modified:app \
"$@"
