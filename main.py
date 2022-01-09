from prometheus_client import start_http_server, Gauge
from xml.etree import ElementTree
import requests
import time

TRAFFIC_CURRENT_DOWNLOAD_RATE = Gauge("hilink_traffic_current_download_rate", "bytes/s")
TRAFFIC_CURRENT_UPLOAD_RATE = Gauge("hilink_traffic_current_upload_rate", "bytes/s")
TRAFFIC_CURRENT_MONTH_DOWNLOAD = Gauge("hilink_traffic_current_month_download", "bits")
TRAFFIC_CURRENT_MONTH_UPLOAD = Gauge("hilink_traffic_current_month_upload", "bits")

start_http_server(9770)

while True:
    r = requests.get("http://192.168.8.1/api/monitoring/traffic-statistics")
    tree = ElementTree.fromstring(r.content)
    TRAFFIC_CURRENT_DOWNLOAD_RATE.set(int(tree.find("CurrentDownloadRate").text))
    TRAFFIC_CURRENT_UPLOAD_RATE.set(int(tree.find("CurrentUploadRate").text))
    r = requests.get("http://192.168.8.1/api/monitoring/month_statistics")
    tree = ElementTree.fromstring(r.content)
    TRAFFIC_CURRENT_MONTH_DOWNLOAD.set(tree.find("CurrentMonthDownload").text)
    TRAFFIC_CURRENT_MONTH_UPLOAD.set(tree.find("CurrentMonthUpload").text)
    time.sleep(30)
