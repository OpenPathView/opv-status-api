from setuptools import setup, find_packages

# Merci Sam & Max : http://sametmax.com/creer-un-setup-py-et-mettre-sa-bibliotheque-python-en-ligne-sur-pypi/

setup(
    name='opv_status_api',
    version='0.0.1',
    packages=find_packages(),
    author="Christophe NOUCHET",
    author_email="team@openpathview.fr",
    description="Open Path View Status Api",
    long_description=open('README.md').read(),
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
    url='https://git.archieri.fr/simon/opv-status-api',
    entry_points={
        'console_scripts': [
            'opv-status-api = opv_status_api.__main__:main']
    },
    scripts=[],

    license="GPL3",
)
