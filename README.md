Wikipedia url route finder

This program could find a route from one url in wikipedia to another. Links must be in
same language.

usage: main.py [-h] [start_url] [end_url] [rate_limit]

positional arguments:
  start_url   url from which the search will begin
  end_url     destination url, where the search must be finished
  rate_limit  number of connections that could be per minute

options:
  -h, --help  show this help message and exit

It's also possible to launch script without arguments. In this case you will be asked for them.
