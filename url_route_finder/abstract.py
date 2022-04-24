from abc import ABC, abstractmethod

class AbstractUrlRouteFinder(ABC):
    def __init__(self, getting_children_urls_from_url_function):
        self.getting_children_urls_from_url_function = getting_children_urls_from_url_function

    def get_children_urls_from_url(self, url):
        return self.getting_children_urls_from_url_function(url)

    @abstractmethod
    def find_url_route(start_url, end_url, route_max_length):
        pass
