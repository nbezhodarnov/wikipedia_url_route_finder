from multiprocessing import Lock, cpu_count
from bs4 import BeautifulSoup
from functools import partial
import urllib.request
import pebble
import time

class AtomicInteger():
    def __init__(self, value=0):
        self._value = int(value)
        self._lock = Lock()
        
    def inc(self, d=1):
        with self._lock:
            self._value += int(d)
            return self._value

    def dec(self, d=1):
        return self.inc(-d)    

    @property
    def value(self):
        with self._lock:
            return self._value

    @value.setter
    def value(self, v):
        with self._lock:
            self._value = int(v)
            return self._value

connection_mutex = Lock()
RATE_LIMIT = 10
actual_connections = AtomicInteger(0)

def safe_url_request(url):
    if (actual_connections.value >= RATE_LIMIT):
        with connection_mutex:
            while (actual_connections.value >= RATE_LIMIT):
                time.sleep(1)
    actual_connections.inc(1)
    url_data = urllib.request.urlopen(url).read()
    actual_connections.dec(1)
    return url_data

def extract_wikipedia_main_content(html_page):
    soup = BeautifulSoup(html_page, "html.parser")
    return soup.find("div", id="bodyContent")

def is_wikipedia_link(link):
    return link.find("wikipedia") != -1

def extract_wikipedia_page_language(link):
    string_index = 0
    
    scheme_separator_index = link.find("://")
    if (scheme_separator_index != -1):
        string_index = scheme_separator_index + 3

    net_loaction_separator_index = link.find("www.", string_index)
    if (net_loaction_separator_index != -1):
        string_index = net_loaction_separator_index + 4

    language_separator_index = link.find(".", string_index)
    if (language_separator_index != -1):
        return link[string_index:language_separator_index]
    return ""

def get_wikipedia_links_in_same_language(html_page_content, language = "en"):
    soup = html_page_content
    links = []

    for link in soup.findAll("a"):
        link_string = link.get("href")

        if (not link_string):
            continue

        if (link_string[0] == "/"):
            link_string = "https://" + language + ".wikipedia.org" + link_string
        elif (link_string[0] == "#"):
            continue
        elif (not is_wikipedia_link(link_string)):
            continue
        elif (extract_wikipedia_page_language(link_string) != language):
            continue

        links.append(link_string)
    return links

def get_wikipedia_links_from_url(url):
    wikipedia_page_language = extract_wikipedia_page_language(url)
    wikipedia_html_page = safe_url_request(url)
    wikipedia_page_main_content = extract_wikipedia_main_content(wikipedia_html_page)
    wikipedia_links = get_wikipedia_links_in_same_language(wikipedia_page_main_content, wikipedia_page_language)
    return wikipedia_links

def find_url_route(start_url, end_url, route_max_length, visited_links = []):
    if (start_url == end_url):
        return [start_url]
    if (route_max_length <= 1):
        return []

    main_route = [start_url]

    try:
        wikipedia_links = get_wikipedia_links_from_url(start_url)
    except Exception as exception:
        return []

    visited_links.append(start_url)

    if end_url in wikipedia_links:
        return [start_url, end_url]

    if (route_max_length == 2):
        return []

    for link in wikipedia_links:
        if (link in visited_links):
            continue
            
        route = find_url_route(link, end_url, route_max_length - 1, visited_links)
        if (route):
            main_route.extend(route)
            return main_route

    return []

def find_url_route_for_one_url_from_list(start_url_list, end_url, route_max_length, visited_links = []):
    if end_url in start_url_list:
        return [end_url]
    
    if (route_max_length <= 1):
        return []

    route = []

    for url in start_url_list:
        route = find_url_route(url, end_url, route_max_length, visited_links)
        if (route):
            break

    return route

def multiprocess_find_url_route(start_url, end_url, route_max_length):
    if (start_url == end_url):
        return [end_url]
    if (route_max_length <= 1):
        return []

    main_route = [start_url]

    try:
        wikipedia_links = get_wikipedia_links_from_url(start_url)
    except Exception as exception:
        return []
    
    if end_url in wikipedia_links:
        return [start_url, end_url]

    visited_links = [start_url]

    cores_count = cpu_count()

    wikipedia_links_sublists = []
    for thread_index in range(cores_count):
        wikipedia_links_sublist = []
        wikipedia_links_index = thread_index
        while (wikipedia_links_index < len(wikipedia_links)):
            wikipedia_links_sublist.append(wikipedia_links[wikipedia_links_index])
            wikipedia_links_index += cores_count
        wikipedia_links_sublists.append(wikipedia_links_sublist)

    route = []
    with pebble.ProcessPool(max_workers = cores_count) as executor:
        future_to_url = executor.map(partial(find_url_route_for_one_url_from_list, end_url = end_url, route_max_length = route_max_length - 1, visited_links = visited_links), [links_sublist for links_sublist in wikipedia_links_sublists])
        for future in future_to_url.result():
            route = future
            if (route):
                executor.stop()
                break

    if (route):
        main_route.extend(route)
    else:
        main_route = []

    return main_route

def main():
    start_url = input("Input start url: ")
    end_url = input("Input end url: ")
    RATE_LIMIT = input("Input rate-limit: ")
    route = multiprocess_find_url_route(start_url, end_url, 5)
    if (route):
        print("Url route: ")
        print(*route, sep=" => ")
    else:
        print("There are no routes for these urls.")

if __name__ == '__main__':
    main()
