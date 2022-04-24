import wikipedia_module
import argparse

INPUT_START_URL_MESSAGE = "Input start url: "
INPUT_END_URL_MESSAGE = "Input end url: "
INPUT_RATE_LIMIT_MESSAGE = "Input rate-limit: "

def force_to_set_positive_int(int_number, message):
    while (int_number <= 0):
        print("Value must be positive!")
        int_number = int(input(message))
    return int_number

def force_to_set_nonempty_url(url, message, print_error_message_first_time = False):
    url_modified = False
    print_error_message = print_error_message_first_time
    while (len(url) <= 0):
        if (print_error_message):
            print("String must be nonempty!")
        else:
            print_error_message = True
        url = input(message)
        url_modified = True
    return url, url_modified

def force_to_set_wikipedia_url(url, message, print_error_message_first_time = False):
    url_modified = False
    print_error_message = print_error_message_first_time
    if (url and not wikipedia_module.is_wikipedia_url(url)):
            print("It must be wikipedia url!")
            print_error_message = False
    while (not wikipedia_module.is_wikipedia_url(url)):
        if (print_error_message):
            print("It must be wikipedia url!")
        else:
            print_error_message = True
        url = ""
        url, url_modified = force_to_set_nonempty_url(url, message)
        url_modified = True
    return url, url_modified

def force_to_set_wikipedia_urls_in_same_language(url1, url2, message1, message2, print_error_message_first_time = True):
    urls_modified = False
    print_error_message = print_error_message_first_time
    while (wikipedia_module.extract_page_language(url1) != wikipedia_module.extract_page_language(url2)):
        if (print_error_message):
            print("Languages of urls are different! Please, use urls in same language!")
        else:
            print_error_message = True
        url1, url2 = "", ""
        url1, url_modified = force_to_set_wikipedia_url(url1, message1)
        url2, url_modified = force_to_set_wikipedia_url(url2, message2)
        urls_modified = True
    return url1, url2, urls_modified

def get_arguments_from_command_line():
    parser = argparse.ArgumentParser(description = "Wikipedia url route finder. This program could find a route from one url in wikipedia to another. Links must be in same language.", exit_on_error = False)
    parser.add_argument("start_url", metavar = "start_url", help = "url from which the search will begin", nargs='?', default = "")
    parser.add_argument("end_url", metavar = "end_url", help = "destination url, where the search must be finished", nargs='?', default = "")
    parser.add_argument("rate_limit", metavar = "rate_limit", type = int, help = "number of connections that could be per minute", nargs='?', default = 10)

    start_url, end_url, rate_limit = "", "", 10

    try:
        arguments = parser.parse_args()
        start_url, end_url, rate_limit = arguments.start_url, arguments.end_url, arguments.rate_limit
    except argparse.ArgumentError:
        print("Unable to read arguments. You will be asked for them.")

    return start_url, end_url, rate_limit

def get_arguments():
    start_url, end_url, rate_limit = get_arguments_from_command_line()

    necessary_to_set_arguments = False
    url_modified = False

    start_url, url_modified = force_to_set_wikipedia_url(start_url, INPUT_START_URL_MESSAGE)
    if (url_modified):
        necessary_to_set_arguments = True

    end_url, necessary_to_set_arguments = force_to_set_wikipedia_url(end_url, INPUT_END_URL_MESSAGE)
    if (url_modified):
        necessary_to_set_arguments = True

    start_url, end_url, url_modified = force_to_set_wikipedia_urls_in_same_language(start_url, end_url, INPUT_START_URL_MESSAGE, INPUT_END_URL_MESSAGE)
    if (url_modified):
        necessary_to_set_arguments = True

    if (necessary_to_set_arguments):
        rate_limit = int(input(INPUT_RATE_LIMIT_MESSAGE))

    rate_limit = force_to_set_positive_int(rate_limit, INPUT_RATE_LIMIT_MESSAGE)

    return start_url, end_url, rate_limit
