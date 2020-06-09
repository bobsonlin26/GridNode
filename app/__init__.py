from flask import Flask
from flask_sockets import Sockets

## added by bobsonlin
import syft as sy
import torch as th
from torchvision import datasets
from torchvision import transforms
import logging
import numpy as np
KEEP_LABELS_DICT = {
    "alice": [0, 1, 2, 3],
    "bob": [4, 5, 6],
    "charlie": [7, 8, 9],
    "testing": list(range(10)),
    None: list(range(10)),
}

## added by bobsonlin
FORMAT = "%(asctime)s | %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger("run_websocket_server")
logger.setLevel(level=logging.DEBUG)


def create_app(node_id, debug=False, database_url=None):
    """ Create / Configure flask socket application instance.

        Args:
            node_id (str) : ID of Grid Node.
            debug (bool) : debug flag.
            test_config (bool) : Mock database environment.
        Returns:
            app : Flask application instance.
    """
    app = Flask(__name__)
    app.debug = True
    # app.debug = debug

    app.config["SECRET_KEY"] = "justasecretkeythatishouldputhere"

    # Enable persistent mode
    # Overwrite syft.object_storage methods to work in a persistent way
    # Persist models / tensors
    if database_url:
        app.config["REDISCLOUD_URL"] = database_url
        from .main.persistence import database, object_storage

        db_instance = database.set_db_instance(database_url)
        object_storage.set_persistent_mode(db_instance)

    from .main import html, ws, hook, local_worker, auth

    # Global socket handler
    sockets = Sockets(app)

    # set_node_id(id)
    local_worker.id = node_id
    hook.local_worker._known_workers[node_id] = local_worker
    # print("###", "local_worker.__class__:", local_worker.__class__, "###")

    ## added by bobsonlin
    local_worker.add_worker(hook.local_worker)
    # print("###", "hook.local_worker.__class__:", hook.local_worker.__class__, "###")

    # Register app blueprints
    app.register_blueprint(html, url_prefix=r"/")
    sockets.register_blueprint(ws, url_prefix=r"/")

    # Set Authentication configs
    app = auth.set_auth_configs(app)

    return app

# python ./grid_node_modified.py --host 0.0.0.0 --port 6666 --id alice --notebook mnist-parallel
# python ./grid_node_modified.py --host 0.0.0.0 --port 6667 --id bob --notebook mnist-parallel
# python ./grid_node_modified.py --host 0.0.0.0 --port 6668 --id charlie --notebook mnist-parallel
# python ./grid_node_modified.py --host 0.0.0.0 --port 6669 --id testing --testing --notebook mnist-parallel
def create_mnist_parallel_app(node_id, debug=False, database_url=None, training=True):
    """ Create / Configure flask socket application instance.

        Args:
            node_id (str) : ID of Grid Node.
            debug (bool) : debug flag.
            test_config (bool) : Mock database environment.
        Returns:
            app : Flask application instance.
    """
    app = Flask(__name__)
    app.debug = debug

    app.config["SECRET_KEY"] = "justasecretkeythatishouldputhere"

    # Enable persistent mode
    # Overwrite syft.object_storage methods to work in a persistent way
    # Persist models / tensors
    if database_url:
        app.config["REDISCLOUD_URL"] = database_url
        from .main.persistence import database, object_storage

        db_instance = database.set_db_instance(database_url)
        object_storage.set_persistent_mode(db_instance)

    from .main import html, ws, hook, local_worker, auth

    # Global socket handler
    sockets = Sockets(app)

    # set_node_id(id)
    local_worker.id = node_id
    hook.local_worker._known_workers[node_id] = local_worker
    # print("###", "local_worker.__class__:", local_worker.__class__, "###")

    ## added by bobsonlin
    local_worker.add_worker(hook.local_worker)
    # print("###", "hook.local_worker.__class__:", hook.local_worker.__class__, "###")

    ## added by bobsonlin
    if training == True:
        key = "mnist"
    else:
        key = "mnist_testing"

    keep_labels = KEEP_LABELS_DICT[local_worker.id]
    mnist_dataset = datasets.MNIST(
        root="./data",
        train=training,
        download=True,
        transform=transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
        ),
    )

    indices = np.isin(mnist_dataset.targets, keep_labels).astype("uint8")
    logger.info("number of true indices: %s", indices.sum())
    selected_data = (
        th.native_masked_select(mnist_dataset.data.transpose(0, 2), th.tensor(indices))
        .view(28, 28, -1)
        .transpose(2, 0)
    )

    logger.info("after selection: %s", selected_data.shape)
    selected_targets = th.native_masked_select(mnist_dataset.targets, th.tensor(indices))

    dataset = sy.BaseDataset(
    data=selected_data, targets=selected_targets, transform=mnist_dataset.transform)

    count = [0] * 10
    for i in range(10):
        count[i] = (dataset.targets == i).sum().item()
        logger.info("      %s: %s", i, count[i])

    local_worker.add_dataset(dataset, key=key)

    # Register app blueprints
    app.register_blueprint(html, url_prefix=r"/")
    sockets.register_blueprint(ws, url_prefix=r"/")

    # Set Authentication configs
    app = auth.set_auth_configs(app)

    return app
