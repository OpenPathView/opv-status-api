# Open Path View Status API
An HTTP rest API which allow [opv-status](https://git.archieri.fr/simon/opv-status) to work.
This API manage Spark and [OPV-importData](https://github.com/OpenPathView/OPV_importData)

## Requirements
This API is made to work with [OPV-Ansible](https://github.com/OpenPathView/OPV_Ansible) which create, configure and install a dev env for OPV

This API work with python3 http.server.
You should install dependencies with pip :

```bash
pip install -r requirements.txt
```

## How to use ?
You must first install the API with
```bash
python3 setup.py develop

#And you can now use launch the api
opv-status-api

#Use --debug to get more INFO
opv-status-api --debug

#You can change API port using --port
opv-status-api --port=5002

#You are lost ?
opv-status-api --help
```

## Endpoint
```
api
├── import
│   ├── launch          POST --> {"path": str, "id_malette": int, "camera_number": int, "description": str, "campaign_name": str, "id_rederbro": str}
│   ├── log             POST --> {"logFile": str}
│   └── status          GET
└── spark
    ├── launch          POST --> {"campaignName": str, "customLaunchScript": str}
    └── port            GET
```

## License
Copyright (C) 2017 Open Path View, Maison Du Libre <br />
This program is free software; you can redistribute it and/or modify  <br />
it under the terms of the GNU General Public License as published by  <br />
the Free Software Foundation; either version 3 of the License, or  <br />
(at your option) any later version.  <br />
This program is distributed in the hope that it will be useful,  <br />
but WITHOUT ANY WARRANTY; without even the implied warranty of  <br />
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the  <br />
GNU General Public License for more details.  <br />
You should have received a copy of the GNU General Public License along  <br />
with this program. If not, see <http://www.gnu.org/licenses/>.  <br />
