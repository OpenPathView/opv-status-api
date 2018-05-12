
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

import time
import logging
from path import Path
from threading import Thread
from opv_import.services import TreatRederbroData
from opv_api_client import RestClient as OpvApiRestClient
from opv_directorymanagerclient import DirectoryManagerClient, Protocol


class ImportDataThread(Thread):
    status = "down"
    doing = "nothing"
    pourcent = 0
    timeStart = 0
    logger = logging.getLogger("opv_status_api")

    def __init__(self, data={"path": "/home/opv/campaign", "id_malette": 1, "camera_number": 6, "campaign_name": "test", "id_rederbro": 1, "description": "A campaign"}):
        self.data = data
        self.timeStart = time.time()

        Thread.__init__(self)

    def run(self):
        self.status = "up"
        self.doing = "make lot"
        try:
            self.logger.debug("Launch import data with data={}".format(self.data))
            treat = TreatRederbroData(
                cam_pictures_dir=Path(self.data["path"]+"/SD"),
                id_malette=int(self.data["id_malette"]),
                opv_api_client=OpvApiRestClient("http://opv_master:5000"),
                opv_dm_client=DirectoryManagerClient(api_base="http://opv_master:5005", default_protocol=Protocol.FTP),
                number_of_cameras=int(self.data["camera_number"]),
                csv_meta_path=Path(self.data["path"]+"/picturesInfo.csv")
            )

            treat.make_lot()
            self.doing = "make campaign"
            treat.create_campaign(name=self.data['campaign_name'], id_rederbro=int(self.data['id_rederbro']), description=self.data['description'])
            self.doing = "save lot"
            treat.save_all_lot(on_progress_listener=self.setProgress)
            self.status = "down"
        except Exception as e:
            self.logger.debug("Error while launching import : {}".format(e))
            self.status = "down"
            self.doing = "Exception : {}".format(e)

    def setProgress(self, progress):
        self.pourcent = progress * 100

    def getInfo(self):
        return {
            "status": self.status,
            "doing": self.doing,
            "pourcent": self.pourcent,
            "time": time.time() - self.timeStart
        }
