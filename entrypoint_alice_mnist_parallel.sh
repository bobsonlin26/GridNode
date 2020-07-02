#!/bin/bash
export ID=alice
export ADDRESS=http://0.0.0.0:6666
export MNIST_PARALLEL=True

exec gunicorn -k flask_sockets.worker grid_node_modified:app \
"$@"
