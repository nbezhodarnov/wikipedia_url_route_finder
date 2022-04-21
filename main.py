from bs4 import BeautifulSoup
from functools import partial
import urllib.request
import argparse
import pebble
import queue
import time

class LastConnectionTime:
    value = time.time()
RATE_LIMIT = 10

def safe_url_request(url):
    time_delay = LastConnectionTime.value - time.time() + 60 / RATE_LIMIT
    if (time_delay > 0):
        time.sleep(time_delay)
    url_data = urllib.request.urlopen(url).read()
    LastConnectionTime.value = time.time()
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

def search_url_route_in_queue(queue, end_url, route_max_length, visited_links):
    main_route = []

    while not queue.empty():
        route = queue.get()
        if (not route or len(route) >= route_max_length):
            continue
        try:
            children_wikipedia_links = get_wikipedia_links_from_url(route[-1])
        except Exception as exception:
            continue

        if (end_url in children_wikipedia_links):
            main_route.extend(route)
            main_route.append(end_url)
            break

        for child_link in children_wikipedia_links:
            if (child_link in visited_links or len(route) >= route_max_length):
                continue
            visited_links.append(child_link)
            queue.put(route + [child_link])

    return main_route

def find_url_route_bfs(start_url, end_url, route_max_length):
    if (start_url == end_url):
        return [start_url]
    if (route_max_length <= 1):
        return []

    links_queue = queue.Queue()
    links_queue.put([start_url])

    visited_links = [start_url]

    return search_url_route_in_queue(links_queue, end_url, route_max_length, visited_links)

def main():
    parser = argparse.ArgumentParser(description = "Wikipedia url route finder. This program could find a route from one url in wikipedia to another. Links must be in same language.", exit_on_error = False)
    parser.add_argument("start_url", metavar = "start_url", help = "url from which the search will begin", nargs='?', default = "")
    parser.add_argument("end_url", metavar = "end_url", help = "destination url, where the search must be finished", nargs='?', default = "")
    parser.add_argument("rate_limit", metavar = "rate_limit", type = int, help = "number of connections that could be per minute", nargs='?', default = 10)
    try:
        arguments = parser.parse_args()
    except argparse.ArgumentError:
        print("Unable to read arguments. You will be asked for them.")
    
    start_url = arguments.start_url
    end_url = arguments.end_url
    RATE_LIMIT = arguments.rate_limit
    
    are_arguments_unset = False
    
    if (start_url == ""):
        are_arguments_unset = True
        start_url = input("Input start url: ")
    
    if (end_url == ""):
        are_arguments_unset = True
        end_url = input("Input end url: ")

    while (extract_wikipedia_page_language(start_url) != extract_wikipedia_page_language(end_url)):
        print("Languages of start_url and end_url are different! Please, use an url in same language (" + extract_wikipedia_page_language(start_url) + ")")
        end_url = input("Input end url: ")

    
    if (are_arguments_unset):
        RATE_LIMIT = int(input("Input rate-limit: "))
    
    while (RATE_LIMIT <= 0):
        print("Value rate-limit must be positive!")
        RATE_LIMIT = int(input("Input rate-limit: "))

    route = find_url_route_bfs(start_url, end_url, 5)
    if (route):
        print("Url route: ")
        print(*route, sep=" => ")
    else:
        print("There are no routes for these urls.")

if __name__ == '__main__':
    main()
