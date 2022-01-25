# Simple Zookeeper Viewer

A simple ZooKeeper viewer web app. Enough said.

## Setup

Requires a Python environment with [kazoo](https://github.com/python-zk/kazoo)
and [Flask](https://github.com/pallets/flask). 
For example, install these requirements via `pip` and the provided `requirements.txt` file:

    pip install -r requirements.txt


## Usage

Launch the web app locally, providing the desired ZooKeeper hosts string 
(`127.0.0.1:2181` by default), for example:

    python viewer.py zk01.example.com:2181,zk02.example.com:2181

Go to http://127.0.0.1:5000/ to start at the root of the ZooKeeper service.
Navigate the tree of ZooKeeper nodes on the left and inspect the corresponding data and metadata on the right.

Optionally, tweak the viewer web app host/port with the options `--port`/`--host`.

## Background

This is a friendly fork of the [original viewer by David Wen](https://github.com/davidwen/simple-zookeeper-viewer). 
It further simplifies the project: same functionality but with fewer templates, 
fewer view functions, no custom CSS, no custom JavaScript.
