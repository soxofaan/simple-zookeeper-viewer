import contextlib
import logging
import os
import sys
from typing import List, NamedTuple

from flask import Flask, render_template
from kazoo.client import KazooClient

ZK_HOSTS_DEFAULT = "127.0.0.1:2181"

log = logging.getLogger("simple-zookeeper-viewer")

app = Flask(__name__)

# Node metadata to view
ZNODESTAT_ATTR = [
    'aversion',
    'ctime',
    'czxid',
    'dataLength',
    'ephemeralOwner',
    'mtime',
    'mzxid',
    'numChildren',
    'version']


@contextlib.contextmanager
def get_zk():
    zk = KazooClient(hosts=app.config.get("ZK_HOSTS", ZK_HOSTS_DEFAULT), read_only=True)
    zk.start()
    yield zk
    zk.stop()
    zk.close()


class ZooPath:
    """Wrapper for ZooKeeper paths and operations."""

    def __init__(self, path: str):
        self._parts = self._parse_path(path)

    @staticmethod
    def _parse_path(path: str) -> List[str]:
        """Normalize a path and split in components"""
        parts = path.strip("/").split("/")
        if parts == [""]:
            parts = ["/"]
        else:
            parts = ["/"] + parts
        return parts

    @staticmethod
    def _join(parts: List[str]) -> str:
        return parts[0] + "/".join(p for p in parts[1:])

    @property
    def name(self):
        return self._parts[-1]

    @property
    def full(self):
        return self._join(self._parts)

    def __str__(self):
        return self.full

    def child(self, name: str) -> "ZooPath":
        return ZooPath(self._join(self._parts + [name]))

    def is_ancestor_of(self, path: "ZooPath"):
        return self._parts == path._parts[:len(self._parts)]


class ZooTree(NamedTuple):
    path: ZooPath
    children: List["ZooTree"]


@app.route('/', defaults={'path': '/'})
@app.route("/tree", defaults={"path": "/"})
@app.route("/tree/", defaults={"path": "/"})
@app.route("/tree/<path:path>")
def tree(path):
    """
    Build tree around given path: ancestors,
    siblings of ancestors and own children
    """
    path = ZooPath(path)

    def get_tree(zk: KazooClient, path: ZooPath, follow: ZooPath) -> ZooTree:
        child_names = zk.get_children(path.full)
        child_paths = [path.child(c) for c in child_names]
        if path.is_ancestor_of(follow):
            children = [get_tree(zk=zk, path=p, follow=follow) for p in child_paths]
        else:
            children = []
        return ZooTree(path=path, children=children)

    with get_zk() as zk:
        tree = get_tree(zk=zk, path=ZooPath("/"), follow=path)
        raw, stat = zk.get(path.full)
        meta = {k: getattr(stat, k) for k in ZNODESTAT_ATTR}
        # TODO: add JSON parsed version

    return render_template(
        'tree.html',
        zk_hosts=app.config.get("ZK_HOSTS", ZK_HOSTS_DEFAULT),
        path=path,
        tree=tree,
        raw=raw,
        meta=meta
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    host = '127.0.0.1'
    port = 5000
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])

    app.config["ZK_HOSTS"] = os.environ.get("ZK_HOSTS", ZK_HOSTS_DEFAULT)

    log.info(f"Using ZK_HOSTS={app.config['ZK_HOSTS']!r}")

    app.run(host=host, port=port, debug=True)
