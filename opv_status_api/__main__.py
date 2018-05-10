from http.server import HTTPServer
from opv_status_api.httpHandler import HttpHandler
import docopt
import logging
import json
from opv_status_api.logging import setup_logging

__doc__ = """
An api for opv-status front
Usage:
    opv-status-api [--port=<int>] [--debug]
    opv-status-api -h
Options:
    -h --help                       Show this screen
    --debug                         Enable debugging options
    --port=<int>                    Set API port [default: 5001]
"""


def main():
    args = docopt.docopt(__doc__)

    setup_logging()
    logger = logging.getLogger("opv_status_api")
    logger.setLevel(logging.DEBUG if "--debug" in args and args["--debug"] else logging.INFO)

    server_address = ('', int(args["--port"]))
    logger.info("Starting http server at http://localhost:{} open to {}".format(server_address[1], server_address[0]))
    httpd = HTTPServer(server_address, HttpHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
