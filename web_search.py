#!/usr/bin/python

import sys
import string
import requests
import re
import time

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

# returns array of search result counts for the 3 question/answer combos
# arg: question, answer1, answer2, answer3 are all strings
def CountQuestionAnswerResults(question, answer1, answer2, answer3):

    counts = []
    counts.append(CountSearchResults(GoogleSearch(question + " " + answer1)))
    counts.append(CountSearchResults(GoogleSearch(question + " " + answer2)))
    counts.append(CountSearchResults(GoogleSearch(question + " " + answer3)))

    return counts


# returns normalized array of search result counts for the 3 question/answer combos
# arg: question, answer1, answer2, answer3 are all strings
def CountNormalizedQuestionAnswerResults(question, answer1, answer2, answer3):

    counts = CountQuestionAnswerResults(question, answer1, answer2, answer3)
    counts[0] /= CountSearchResults(GoogleSearch(answer1))
    counts[1] /= CountSearchResults(GoogleSearch(answer2))
    counts[2] /= CountSearchResults(GoogleSearch(answer3))

    return counts

# returns array of search result counts for the 3 question/answer combos and normalized counts
# arg: question, answer1, answer2, answer3 are all strings
def CountBothQuestionAnswerResults(question, answer1, answer2, answer3):

    counts = CountQuestionAnswerResults(question, answer1, answer2, answer3)
    counts.append(counts[0] / CountSearchResults(GoogleSearch(answer1)))
    counts.append(counts[1] / CountSearchResults(GoogleSearch(answer2)))
    counts.append(counts[2] / CountSearchResults(GoogleSearch(answer3)))

    return counts


### MAIN ###



question = "Who was the third president of the United States?"
answer1 = "Abraham Lincoln"
answer2 = "Thomas Jefferson"
answer3 = "George Washington"

start_time = time.time()

#counts = CountQuestionAnswerResults(question, answer1, answer2, answer3)
#normalized_counts = CountNormalizedQuestionAnswerResults(question, answer1, answer2, answer3)
counts = CountBothQuestionAnswerResults(question, answer1, answer2, answer3)
normalized_counts = []
normalized_counts.append(counts[3])
normalized_counts.append(counts[4])
normalized_counts.append(counts[5])

print (question)
print ("---Search Counts---")
print (answer1 + ": " + str(counts[0]))
print (answer2 + ": " + str(counts[1]))
print (answer3 + ": " + str(counts[2]))
print ("---Normalized Search Counts---")
print (answer1 + ": " + str(normalized_counts[0]))
print (answer2 + ": " + str(normalized_counts[1]))
print (answer3 + ": " + str(normalized_counts[2]))
print ("Lookup took " + str(time.time() - start_time) + " seconds.")
