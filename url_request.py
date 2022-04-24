import urllib.request
import time

class LastConnectionTime:
    value = time.time()
RATE_LIMIT = 10

def url_request_with_rate_limit(url):
    time_delay = LastConnectionTime.value - time.time() + 60 / RATE_LIMIT
    if (time_delay > 0):
        time.sleep(time_delay)

    url_data = urllib.request.urlopen(url).read()
    LastConnectionTime.value = time.time()
    return url_data
