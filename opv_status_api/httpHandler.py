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
        self.end_headers()
        self.wfile.write(json.dumps(answer["answer"]).encode())
