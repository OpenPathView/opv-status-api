# coding: utf-8

# Copyright (C) 2017 Open Path View, Maison Du Libre
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

# Contributors: Simon Archieri <simon.archieri@openpathview.fr>
# Email: team@openpathview.fr
# Description: OPV status api

from http.server import HTTPServer
from opv_status_api.httpHandler import HttpHandler
import docopt
import logging
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
