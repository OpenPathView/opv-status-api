#!/usr/bin/env python
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

from setuptools import setup, find_packages

# Merci Sam & Max : http://sametmax.com/creer-un-setup-py-et-mettre-sa-bibliotheque-python-en-ligne-sur-pypi/

setup(
    name='opv_status_api',
    version='0.0.1',
    packages=find_packages(),
    author="Christophe NOUCHET",
    author_email="team@openpathview.fr",
    description="Open Path View Status Api",
    dependency_links=[
        "git+https://github.com/OpenPathView/DirectoryManagerClient@stable#egg=opv_directorymanagerclient",
        "git+https://github.com/OpenPathView/OPV_DBRest-client@stable#egg=opv_api_client",
        "git+https://github.com/OpenPathView/OPV_importData/@master#egg=opv_import"
    ],
    install_requires=[
        "path.py",
        "psutil",
        "opv_import",
        "opv_directorymanagerclient",
        "opv_api_client",
        "docopt",
        "PyYAML"
    ],
    # Active la prise en compte du fichier MANIFEST.in
    include_package_data=True,
    url='https://github.com/OpenPathView/opv-status-api',
    entry_points={
        'console_scripts': [
            'opv-status-api = opv_status_api.__main__:main']
    },
    scripts=[],

    license="GPL3",
)
