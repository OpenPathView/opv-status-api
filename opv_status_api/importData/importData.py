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

import os
import copy
import logging
from opv_status_api.importData.importDataThread import ImportDataThread


class ImportData:
    logger = logging.getLogger("opv_status_api")

    defaultLogFile = "/tmp/importData.log"

    importDataThread = ImportDataThread()

    def getStatus(self):
        return {
            "answer": self.importDataThread.getInfo(),
            "error": None
        }

    def launchImport(self, data):
        output = {
            "answer": None,
            "error": None
        }
        if "path" in data and "id_malette" in data and "camera_number" in data and "description" in data and "campaign_name" in data and "id_rederbro" in data:
            self.importDataThread = ImportDataThread(data=data)
            self.importDataThread.start()

            output["answer"] = "Launched, you should check status to know if it work"
        else:
            output["error"] = "Missing param"

        return output

    def getLog(self, data):
        output = {
            "answer": None,
            "error": None
        }
        logFile = self.defaultLogFile if "logFile" not in data else data["logFile"]

        if os.path.isfile(logFile):
            with open(logFile) as log:
                output["answer"] = log.read()

        else:
            output["error"] = "Log file not found"

        return output