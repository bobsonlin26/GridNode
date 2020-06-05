#!/bin/bash
exec gunicorn -k flask_sockets.worker gridnode.__main__:app \
"$@"
