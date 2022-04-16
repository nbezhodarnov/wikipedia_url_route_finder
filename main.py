from bs4 import BeautifulSoup
import urllib.request

def extract_wikipedia_main_content(html_page):
    soup = BeautifulSoup(html_page, "html.parser")
    return soup.find("div", id="bodyContent")

def get_links_list(html_page_content):
    soup = html_page_content
    links = []
    for link in soup.findAll("a"):
        link_string = link.get("href")
        if (link_string and link_string[0] == "/"):
            link_string = "https://www.wikipedia.org" + link_string
        links.append(link_string)
    return links

def find_url_route(start_url, end_url, route_max_length):
    if (route_max_length <= 1):
        return []
    
    main_route = [start_url]

    try:
        wikipedia_html_page = urllib.request.urlopen(start_url)
        wikipedia_page_main_content = extract_wikipedia_main_content(wikipedia_html_page)
        wikipedia_links = get_links_list(wikipedia_page_main_content)
    except ValueError as exception:
        return []
    except (TypeError, NameError):
        return []
    except Exception as exception:
        return []

    for link in wikipedia_links:
        if (not link):
            continue
        if (link == end_url):
            return [start_url, end_url]

        if (route_max_length > 2):
            route = find_url_route(link, end_url, route_max_length - 1)
            if (route):
                main_roure.append(route)
                return main_route

    return []

def main():
    start_url = input("Input start url: ")
    end_url = input("Input end url: ")
    route_max_length_string = input("Input url route max length: ")
    route = find_url_route(start_url, end_url, int(route_max_length_string))
    if (route):
        print("Url route: ")
        print(route, sep=" => ")
    else:
        print("There are no routes for these urls.")

main()
