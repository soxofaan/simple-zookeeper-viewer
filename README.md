### simple-zookeeper-viewer

A simple ZooKeeper viewer. Enough said.

#### Setup

Requires [kazoo](https://github.com/python-zk/kazoo) and [Flask](https://github.com/pallets/flask)

Requirements can be installed via `pip` and the provided `requirements.txt` file.

    $ pip install -r requirements.txt

#### Configuration

The default ZooKeeper host to connect to is `127.0.0.1:2181`.
Override the hosts string through setting the environment variable `ZK_HOSTS`
(or editing it in `viewer.py`)
before running the app.

#### Usage

To run simple-zookeeper-viewer, execute

    $ python viewer.py [host] [port]

Then navigate to http://localhost:5000/ to view the root of the ZooKeeper server.

* Click on a node to view data and metadata on that node
* Double click on a node to view that node and its children
