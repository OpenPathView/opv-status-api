from threading import Thread
import subprocess
import os


class LaunchSparkThread(Thread):
    def __init__(self, launchScript="/home/opv/dev/launch.sh", campaignName=""):
        self.launchScript = launchScript
        self.campaignName = campaignName

        self.launchScriptDir = self.launchScript.split("/")
        del self.launchScriptDir[-1]
        self.launchScriptDir = "/".join(self.launchScriptDir)

        Thread.__init__(self)

    def run(self):
        devnull = open(os.devnull, 'w')
        subprocess.call([self.launchScript, self.campaignName], cwd=self.launchScriptDir, stdout=devnull, stderr=devnull)
        devnull.close()
