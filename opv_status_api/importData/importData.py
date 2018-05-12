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

import copy
import logging
from opv_status_api.importData.importDataThread import ImportDataThread


class ImportData:
    defaultOutput = {
        "httpCode": 200,
        "answer": {
            "error": None,
            "answer": {}
        }
    }

    logger = logging.getLogger("opv_status_api")

    defaultLogFile = "/tmp/importData.log"

    importDataThread = ImportDataThread()

    def getStatus(self, path=[], data={}, type="GET"):
        output = copy.deepcopy(self.defaultOutput).copy()

        if type == "GET":
            info = self.importDataThread.getInfo()

            output["answer"]["answer"] = info

        else:
            output["httpCode"] = 400
            output["answer"]["error"] = "You must use GET"

        return output

    def launchImport(self, path=[], data={}, type="POST"):
        output = copy.deepcopy(self.defaultOutput).copy()

        if type == "POST":
            if "path" in data and "id_malette" in data and "camera_number" in data and "description" in data and "campaign_name" in data and "id_rederbro" in data:
                self.importDataThread = ImportDataThread(data=data)
                self.importDataThread.start()

                output["answer"]["answer"] = "Launched, you should check status to know if it work"
            else:
                output["httpCode"] = 400
                output["answer"]["error"] = "You must set all param"

        else:
            output["httpCode"] = 400
            output["answer"]["error"] = "You must use POST"

        return output

    command = {
        "status": getStatus,
        "launch": launchImport
    }

    def newCommand(self, path=[], data={}, type="GET"):
        if path[0] in self.command:
            self.logger.debug("Launch command {} with path={}, data={}, type={}".format(path[0], path, data, type))
            return self.command[path[0]](self, path=path, data=data, type=type)
        else:
            self.logger.debug("Asked ressource ({}) can't be find in importData".format(path[0]))
            output = copy.deepcopy(self.defaultOutput).copy()
            output["httpCode"] = 400
            output["answer"]["error"] = "We can't find {}".format(path[0])
            return output
