import contextlib
import json
import logging
import os
import sys

from flask import Flask, render_template, jsonify, request
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
    zk = KazooClient(hosts=app.config["ZK_HOSTS"], read_only=True)
    zk.start()
    yield zk
    zk.stop()
    zk.close()


@app.route('/', defaults={'path': ''})
@app.route('/zk/', defaults={'path': ''})
@app.route('/zk/<path:path>')
def view(path):
    return render_template('zk.html', path=path, host=app.config["ZK_HOSTS"])

@app.route('/nodes/', defaults={'path': ''})
@app.route('/nodes/<path:path>')
def nodes(path):
    ancestors = []
    full_path = ''
    ancestors.append({
        'name': '/',
        'full_path': '/'})
    for ancestor in path.split('/'):
        if ancestor != '':
            full_path += '/' + ancestor
            ancestors.append({
                'name': ancestor,
                'full_path': full_path})
    with get_zk() as zk:
        children = sorted(zk.get_children(path))
    return render_template('_nodes.html',
        path=full_path + '/',
        children=children,
        ancestors=ancestors)

@app.route('/data/', defaults={'path': ''})
@app.route('/data/<path:path>')
def data(path):
    with get_zk() as zk:
        node = zk.get(path)
    meta = {}
    for attr in ZNODESTAT_ATTR:
        meta[attr] = getattr(node[1], attr)
    if path.endswith('/'):
        path = path[:-1]
    data = parse_data(node[0])
    return render_template('_data.html',
        path='/' + path,
        data=data,
        is_dict=type(data) == dict,
        meta=meta);

def parse_data(raw_data):
    try:
        data = json.loads(raw_data)
        return data
    except:
        return repr(raw_data)


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


