# Simple Zookeeper Viewer

A simple ZooKeeper viewer web app. Enough said.

## Setup

Requires a Python environment with [kazoo](https://github.com/python-zk/kazoo)
and [Flask](https://github.com/pallets/flask). 
For example, install these requirements via `pip` and the provided `requirements.txt` file:

    pip install -r requirements.txt

## Configuration

By default, the viewer visualizes the ZooKeeper service at `127.0.0.1:2181`. 
Override this hosts string through setting the environment variable `ZK_HOSTS` (or editing it in `viewer.py`)
before running the app.

## Usage

Launch the web app locally:

    python viewer.py

Go to http://127.0.0.1:5000/ to start at the root of the ZooKeeper service.
Navigate the tree of ZooKeeper nodes on the left and inspect the corresponding data and metadata on the right.


## Background

This is friendly fork of the [original viewer by David Wen](https://github.com/davidwen/simple-zookeeper-viewer). 
It further simplifies the project: same functionality but with fewer templates, 
fewer view functions, less CSS, less JavaScript.
