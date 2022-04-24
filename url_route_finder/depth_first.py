from url_route_finder.abstract import AbstractUrlRouteFinder

class DepthFirstUrlRouteFinder(AbstractUrlRouteFinder):
    def __init__(self, getting_children_urls_from_url_function):
        self.__visited_links = []
        super().__init__(getting_children_urls_from_url_function)

    def __find_url_route(self, start_url, end_url, route_max_length):
        if (start_url == end_url):
            return [start_url]
        if (route_max_length <= 1):
            return []

        main_route = []

        try:
            children_urls = self.get_children_urls_from_url(start_url)
        except Exception as exception:
            return []

        self.__visited_links.append(start_url)

        if end_url in children_urls:
            return [start_url, end_url]

        if (route_max_length == 2):
            return []

        for url in children_urls:
            if (url in self.__visited_links):
                continue

            route = self.__find_url_route(url, end_url, route_max_length - 1)
            if (route):
                main_route.append(start_url)
                main_route.extend(route)
                break

        return main_route

    def find_url_route(self, start_url, end_url, route_max_length):
        url_route = self.__find_url_route(start_url, end_url, route_max_length)
        self.__visited_links.clear()
        return url_route
