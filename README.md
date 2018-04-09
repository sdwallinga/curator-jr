# curator-jr

*...a dollar-store ElasticSearch archival tool*

## Requirements
* Python3 
* python-elasticsearch: `pip3 install elasticsearch`
* Elasticdump from NPM: `npm install -g elasticdump`

NOTE: The latest release of elasticdump, `3.3.8`, has dropped support for node.js versions less than 8. There are two options: upgrade Node, or `npm install -g elasticdump@3.3.7`.

## Installation

* Change the `name_prefix` and `haproxy_ip'' variable to reflect the customer's environment. 
* Change the `sla_days` variable to reflect the number of days the customer requires in their ElasticSearch cluster
* Change the `archive_directory` variable to point to the directory you'd like to stash files. (This is typically `/storage` on an NFS mount).

## Usage

Recommend running this in a `tmux` session and leaving it alone.

`python3 curator-jr.py`

That's it!

