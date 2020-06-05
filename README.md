![foobar-logo](https://raw.githubusercontent.com/OpenMined/design-assets/master/logos/PyGrid/horizontal-primary-trans.png)

![Tests](https://github.com/OpenMined/GridNode/workflows/Run%20tests/badge.svg)
![License](https://img.shields.io/github/license/OpenMined/GridNode)
![OpenCollective](https://img.shields.io/opencollective/all/openmined)

# GridNode

GridNode helps to data owners manage their data, being the place where data lives. It is part of the [PyGrid Platform](https://github.com/OpenMined/PyGrid/):
- PyGrid.  A server based application used to manage/monitor/control and route grid Nodes/Workers remotely.
- **GridNode**. A server based application used to store and manage data access in a secure and private way.
- GridWorkers. Clientd based app that uses different Syft based libraries to perform federated learning (ex: syft.js, KotlinSyft, SwiftSyft).


## Installation

Use the package manager pip to install GridNode

```bash
git clone https://github.com/OpenMined/GridNode
pip install .
```

## Usage

```bash
python -m gridnode <arguments>
```
You can pass the arguments or use environment variables to set the gateway configs.  

**Arguments**
```
  -h, --help                shows the help message and exit
  --id ID                   Grid node ID, e.g. --id=alice. Default is
                            os.environ.get('GRID_WS_ID', None).

  --port PORT, -p PORT      Port number of the socket.io server, e.g. --port=8777.
                            Default is os.environ.get('GRID_WS_PORT', None).

  --host HOST               Grid node host, e.g. --host=0.0.0.0.
                            Default is os.environ.get('GRID_WS_HOST','http://0.0.0.0').

  --gateway_url GATEWAY_URL Address used to join a Grid Network. This argument isoptional.
                            Default is os.environ.get('GRID_NETWORK_URL', None).

  --db_url DB_URL           REDIS database server address
```

**Environment Variables**
- `GRID_GATEWAY_PORT` -  Port to run server on.
- `GRID_GATEWAY_HOST` - The grid gateway host
- `NUM_REPLICAS` - Number of replicas to provide fault tolerance to model hosting
- `DATABASE_URL` - The gateway database URL
- `SECRET_KEY` - The secret key

Example:

```bash
python -m gridnode --id=alice --port=5000
```



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Contributors

Please make sure to fill this section in with **all former and current** contributors to the project. [Documentation on how to do this is located here.](https://github.com/all-contributors/all-contributors)

## License
[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)