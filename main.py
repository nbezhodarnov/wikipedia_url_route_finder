from url_route_finder.breadth_first import BreadthFirstUrlRouteFinder
import arguments_parser
import wikipedia_module
import url_request

def main():
    start_url, end_url, url_request.RATE_LIMIT = arguments_parser.get_arguments()

    url_route_finder = BreadthFirstUrlRouteFinder(wikipedia_module.get_children_urls_from_url)
    route = url_route_finder.find_url_route(start_url, end_url, 5)
    if (route):
        print("Url route: ")
        print(*route, sep=" => ")
    else:
        print("There are no routes for these urls.")

if __name__ == '__main__':
    main()
