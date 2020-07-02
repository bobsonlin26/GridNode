#!/bin/bash
export ID=testing
export ADDRESS=http://0.0.0.0:6669
export MNIST_PARALLEL=True
export TESTING=True

exec gunicorn -k flask_sockets.worker grid_node_modified:app \
"$@"
