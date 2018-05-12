from threading import Thread
from path import Path
from opv_import.services import TreatRederbroData
from opv_api_client import RestClient as OpvApiRestClient
from opv_directorymanagerclient import DirectoryManagerClient, Protocol
import time

class ImportDataThread(Thread):
    status = "down"
    doing = "nothing"
    pourcent = 0
    timeStart = 0

    def __init__(self, data={"path": "/home/opv/campaign", "id_malette": 1, "camera_number": 6, "campaign_name": "test", "id_rederbro": 1, "description": "A campaign"}):
        self.data = data
        self.timeStart = time.time()
        Thread.__init__(self)

    def run(self):
        self.status = "up"
        self.doing = "make lot"
        try:
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
            self.status = "down"
            self.doing = "Exception : {}".format(e)

    def setProgress(self, progress):
        self.pourcent = progress * 100

    def getInfo(self):
        return self.status, self.doing, self.pourcent, time.time() - self.timeStart
