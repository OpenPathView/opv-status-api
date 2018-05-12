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

from opv_status_api.spark.launchSparkThread import LaunchSparkThread
import copy
import psutil
import logging


class Spark:
    defaultOutput = {
        "httpCode": 200,
        "answer": {
            "error": None,
            "answer": {}
        }
    }

    logger = logging.getLogger("opv_status_api")

    def getPort(self):
        port = []

        open_connections = psutil.net_connections()

        for connection in open_connections:
            app = psutil.Process(connection.pid)
            if app.name() == "java" and app.username() == "opv" and connection.laddr.ip == "::":
                port.append(connection.laddr.port)

        return port

    def getSparkPort(self, path=[], data={}, type="GET"):
        output = copy.deepcopy(self.defaultOutput).copy()
        if type == "GET":
            output["answer"]["answer"] = self.getPort()
        else:
            output["httpCode"] = 400
            output["answer"]["error"] = "You must use GET"

        return output

    def launchSpark(self, path=[], data={}, type="POST"):
        output = copy.deepcopy(self.defaultOutput).copy()

        if type == "POST":
            if "campaignName" in data:
                self.sparkThread = LaunchSparkThread(campaignName=data["campaignName"])

                if "customLaunchScript" in data:
                    self.sparkThread = LaunchSparkThread(launchScript=data["customLaunchScript"], campaignName=data["campaignName"])

                self.sparkThread.start()

                output["answer"]["answer"] = "Spark launched you should check the api"
            else:
                output["httpCode"] = 400
                output["answer"]["error"] = "You must set the campaign name"

        else:
            output["httpCode"] = 400
            output["answer"]["error"] = "You must use POST"

        return output

    command = {
        "launch": launchSpark,
        "port": getSparkPort
    }

    def newCommand(self, path=[], data={}, type="GET"):
        if path[0] in self.command:
            self.logger.debug("Launch command {} with path={}, data={}, type={}".format(path[0], path, data, type))
            return self.command[path[0]](self, path=path, data=data, type=type)
        else:
            self.logger.debug("Asked ressource ({}) can't be find in Spark".format(path[0]))
            output = copy.deepcopy(self.defaultOutput).copy()
            output["httpCode"] = 400
            output["answer"]["error"] = "We can't find {}".format(path[0])
            return output
