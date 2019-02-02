from flask import Flask, request, abort
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from opv_status_api.importData.importData import ImportData
from opv_status_api.spark.spark import Spark
from opv_status_api.celery.celery import Celery
import json


class Service:
  def __init__(self, host="", port=5001):
    self.port = port
    self.host = host

  def start(self):
    app = Flask("opv-status-api")
    CORS(app)

    importService = ImportData()
    spark = Spark()
    celery = Celery()

    mimetype = {'Content-Type': 'application/json'}

    service = {
      "import": {
        "log": (importService.getLog, "POST"),
        "launch": (importService.launchImport, "POST"),
        "status": (importService.getStatus, "GET")
      },
      "spark": {
        "launch": (spark.launchSpark, "POST"),
        "port": (spark.getSparkPort, "GET")
      },
      "celery": {
        "launch": (celery.LaunchCelery, "POST")
      }
    }

    def check_args(service_name, command_name):
      if (service_name in service and
          command_name in service[service_name]):
        if request.method == service[service_name][command_name][1]:
          return
        abort(405)
      abort(404)

    @app.route("/<string:service_name>/<string:command_name>", methods=["POST", "GET"])
    def launchCommand(service_name, command_name):
      check_args(service_name, command_name)
      if request.method == "POST":
        answer = service[service_name][command_name][0](json.loads(request.data.decode()))
      else:
        answer = service[service_name][command_name][0]()
        
      return json.dumps(answer), 400 if answer["error"] else 200, mimetype 

    http_server = WSGIServer((self.host, self.port), app)
    http_server.serve_forever()