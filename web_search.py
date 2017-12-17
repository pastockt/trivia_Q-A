#!/usr/bin/python

import sys
import string
import requests
import re

base_url = "http://www.google.com/search?"
query = "q="
quote_query = "as_epq="
not_query = "as_eq="

# Return number of search results as int
# arg: search_result_html = html result from GET of google search
def CountSearchResults(search_result_html):

    # Find where the search result number starts in the html string
    result_num_prefix = ">About "
    result_num_char_index = search_result_html.find(result_num_prefix) + len(result_num_prefix)

    # Convert the search result number to an integer
    # TODO: this code sucks. Python definitely has a better way
    result_num_char_array = []

    # Append each digit to the char array, skipping commas
    while (search_result_html[result_num_char_index].isdigit() or search_result_html[result_num_char_index] == ","):

        if (search_result_html[result_num_char_index].isdigit()):
            result_num_char_array.append(search_result_html[result_num_char_index])

        result_num_char_index += 1

    return int("".join(result_num_char_array))


# Return html text from google search
# arg: search query for google search
def GoogleSearch(string):

    query_arg = string.replace(" ", "+")
    return requests.get(base_url + query + query_arg).text


# returns html text from google search (in quotes)
# arg: search query for google search
def GoogleSearchInQuotes(string):

    query_arg = string.replace(" ", "+")
    return requests.get(base_url + quote_query + query_arg).text



print (CountSearchResults(GoogleSearch("tin cans")))
print (CountSearchResults(GoogleSearchInQuotes("tin cans")))

