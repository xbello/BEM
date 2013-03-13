import itertools
import operator
import sys

SORT_KEY = 5

def sort_file(input_file):
    '''Read a file and put the lines as needed.'''
    HSPs = []
    chromosomes = []
    elements = []

    with open(input_file, "r") as input_handler:
        for line in input_handler.readlines():
            splitted_line = line.split()
            splitted_line[SORT_KEY] = int(splitted_line[SORT_KEY])
            HSPs.append(splitted_line)
            if splitted_line[4] not in chromosomes:
                chromosomes.append(splitted_line[4])
            if splitted_line[9] not in elements:
                elements.append(splitted_line[9])

    chromosomes.sort()
    elements.sort()

    return list(
        itertools.chain(*sort_parsed_blast(HSPs, chromosomes, elements)))

def sort_it(match_list, sort_key=SORT_KEY):
    '''Sort a list with the key column'''
    match_list.sort(key=operator.itemgetter(sort_key))

    for x in match_list:
        x[sort_key] = str(x[sort_key])

    return match_list

def sort_parsed_blast(HSPs, chromosomes, elements):
    '''This makes the sort of the first output from BLAST.

    In the first sort, we aim to sort the HSP of a chromosome by element,
    and then by insertion point. This way we allow the joining of HSPs
    even if some of them are overlapping.
    '''

    sorted_lines = []
    for element in elements:
        for chromosome in chromosomes:
            direct_matches = [x for x in HSPs if \
                x[8] == "+" and x[9] == element and x[4] == chromosome]
            reverse_matches = [x for x in HSPs if \
                x[8] == "C" and x[9] == element and x[4] == chromosome]

            if direct_matches:
                sorted_lines.append(sort_it(direct_matches))
            if reverse_matches:
                sorted_lines.append(sort_it(reverse_matches))

    return sorted_lines 
