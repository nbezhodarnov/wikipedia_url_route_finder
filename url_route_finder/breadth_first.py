from url_route_finder.abstract import AbstractUrlRouteFinder
from queue import Queue

class BreadthFirstUrlRouteFinder(AbstractUrlRouteFinder):
    def __init__(self, getting_children_urls_from_url_function):
        self.__visited_links = []
        self.__queue = Queue()
        super().__init__(getting_children_urls_from_url_function)

    def __search_url_route_in_queue(self, end_url, route_max_length):
        main_route = []

        while self.__queue:
            route = self.__queue.get()
            if (len(route) <= 0):
                continue

            try:
                children_urls = self.get_children_urls_from_url(route[-1])
            except Exception as exception:
                continue

            if (end_url in children_urls):
                main_route.extend(route)
                main_route.append(end_url)
                break

            for child_link in children_urls:
                if (child_link in self.__visited_links or len(route) >= route_max_length - 1):
                    continue
                self.__visited_links.append(child_link)
                self.__queue.put(route + [child_link])

        return main_route

    def __find_url_route(self, start_url, end_url, route_max_length):
        if (start_url == end_url):
            return [start_url]
        if (route_max_length <= 1):
            return []

        self.__queue.put([start_url])

        self.__visited_links.append(start_url)

        return self.__search_url_route_in_queue(end_url, route_max_length)

    def find_url_route(self, start_url, end_url, route_max_length):
        url_route = self.__find_url_route(start_url, end_url, route_max_length)
        self.__visited_links.clear()
        self.__queue = Queue()
        return url_route
