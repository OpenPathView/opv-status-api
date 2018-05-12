import os
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

            output["answer"]["answer"]["status"] = info[0]
            output["answer"]["answer"]["doing"] = info[1]
            output["answer"]["answer"]["pourcent"] = info[2]
            output["answer"]["answer"]["time"] = info[3]

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
