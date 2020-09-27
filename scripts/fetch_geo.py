import tarfile
import requests
import shutil
import configparser

from pyasn import mrtx, __version__

maxmind_conf = ConfigParser.RawConfigParser()
maxmind_conf.read('../maxmind.conf')

LICENSE_KEY = maxmind_conf.get('license', 'license_key')

APP_BASE = "/tmp"

if __name__ == '__main__':
    url = "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key={0}&suffix=tar.gz".format(LICENSE_KEY)
    response = requests.get(url)
    path = '%s/GeoLite2-City.tar.gz' % (APP_BASE)
    open(path, 'wb').write(response.content)
    tar = tarfile.open(path)
    files = tar.getmembers()
    tar.extractall(path='/tmp/')
    tar.close()

    for file in files:
        if not file.name.endswith('.mmdb'):
            continue
        shutil.move('/tmp/%s' % file.name, '/tmp/GeoLite2-City.mmdb')
