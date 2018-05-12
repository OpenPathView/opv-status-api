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
