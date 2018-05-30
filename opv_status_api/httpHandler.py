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

from http.server import BaseHTTPRequestHandler
from opv_status_api.importData.importData import ImportData
from opv_status_api.spark.spark import Spark
import json
import logging


class HttpHandler(BaseHTTPRequestHandler):
    importData = ImportData()
    spark = Spark()
    logger = logging.getLogger("opv_status_api")

    def do_GET(self):
        self.logger.info("New GET request at {}".format(self.path))
        asked = self.path.split("/")
        del asked[0]

        if asked[0] == "import" and len(asked) >= 2:
            del asked[0]
            answer = self.importData.newCommand(path=asked, type=self.command)
        elif asked[0] == "spark" and len(asked) >= 2:
            del asked[0]
            answer = self.spark.newCommand(path=asked, type=self.command)
        else:
            answer = {
                "httpCode": 404,
                "answer": {
                    "error": "404",
                    "answer": "This api work =). But you look lost"
                }
            }

        self.logger.debug("Answer of task : {}".format(answer))
        self.send_response(answer["httpCode"])
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(answer["answer"]).encode())

    def do_POST(self):
        self.logger.info("New GET request at {}".format(self.path))
        asked = self.path.split("/")
        del asked[0]

        data = json.loads(self.rfile.read(int(self.headers.get("Content-Length"))).decode())

        if asked[0] == "import" and len(asked) >= 2:
            del asked[0]
            answer = self.importData.newCommand(path=asked, type=self.command, data=data)
        elif asked[0] == "spark" and len(asked) >= 2:
            del asked[0]
            answer = self.spark.newCommand(path=asked, type=self.command, data=data)
        else:
            answer = {
                "httpCode": 404,
                "answer": {
                    "error": "404",
                    "answer": "This api work =). But you look lost"
                }
            }

        self.logger.debug("Answer of task : {}".format(answer))
        self.send_response(answer["httpCode"])
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(answer["answer"]).encode())
