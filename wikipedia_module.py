from bs4 import BeautifulSoup
import url_request

def is_wikipedia_url(url):
    return url.find("wikipedia.org") != -1

def extract_page_language(link):
    language_separator_start_index = 0

    scheme_separator = "://"
    scheme_separator_index = link.find(scheme_separator)
    if (scheme_separator_index != -1):
        language_separator_start_index = scheme_separator_index + len(scheme_separator)

    language_separator_end_index = link.find(".", language_separator_start_index)
    if (language_separator_end_index != -1):
        return link[language_separator_start_index:language_separator_end_index]
    return ""

def extract_main_content(html_page):
    soup = BeautifulSoup(html_page, "html.parser")
    return soup.find("div", id="bodyContent")

def is_relative_url(url):
    return url[0] == "/"

def is_anchor_url(url):
    return url[0] == "#"

def not_wikipedia_url_or_different_language(url, language):
    if (is_anchor_url(url)):
        return True
    elif (not is_wikipedia_url(url)):
        return True
    elif (extract_page_language(url) != language):
        return True
    return False

def generate_absolute_url_from_relative(relative_url, language = "en"):
    scheme = "https://"
    domain_name = "wikipedia.org"

    absolute_url = ""

    if (language):
        absolute_url = scheme + language + "." + domain_name + relative_url
    else:
        absolute_url = scheme + domain_name + relative_url

    return absolute_url

def get_urls_in_same_language(html_page_content, language = "en"):
    soup = html_page_content
    urls = []

    for url in soup.findAll("a"):
        url_string = url.get("href")

        if (not url_string):
            continue

        if (is_relative_url(url_string)):
            url_string = generate_absolute_url_from_relative(url_string, language)

        if (not_wikipedia_url_or_different_language(url_string, language)):
            continue

        urls.append(url_string)
    return urls

def get_children_urls_from_url(url):
    language = extract_page_language(url)
    html_page = url_request.url_request_with_rate_limit(url)
    main_content = extract_main_content(html_page)
    children_urls = get_urls_in_same_language(main_content, language)
    return children_urls
