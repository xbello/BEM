#!/usr/bin/env python
import operator
import sys

from defs import *

"""This script simply takes a sorted output and cut the elements if two
sequences seems to be ocupying the same spot.
"""

def adjust_score(element, old_length):
    """list, int -> (list)

    Adjust the new score of a post-cut element. We are going to assume that 
    every base of the match provides the same amount of score.
    """
    old_score = float(element[0])
    
    score_per_base = 0.0
    if old_score > 0:
        score_per_base = old_score / old_length

    new_length = abs(int(element[END_Q_POINT]) - \
                 int(element[INIT_Q_POINT]))

    element[0] = "{0:.1f}".format(new_length * score_per_base)

    return element
   

def cut_elements_by_group(elements, top_element):
    """list of lists, list -> (list of lists)

    Takes a best (or top) element and cut all the other in the list by
    it. Returns the remaining of the elements"""

    return_list = []

    for element in elements:
        # First we save the element original length to readjust the score
        # further on
        element_length = abs(int(element[END_Q_POINT]) - \
            int(element[INIT_Q_POINT]))

        if int(element[INIT_Q_POINT]) < int(top_element[INIT_Q_POINT]) and\
           int(element[END_Q_POINT]) > int(top_element[INIT_Q_POINT]) and\
           int(element[END_Q_POINT]) < int(top_element[END_Q_POINT]):
            # Element start before reference, overlaps with it, ends before
            # -> Cut the tail
            element[END_Q_POINT] = str(int(top_element[INIT_Q_POINT]) - 1)
            element[END_S_POINT] = str(int(top_element[INIT_S_POINT]) - 1)
            

        elif int(element[INIT_Q_POINT]) > int(top_element[INIT_Q_POINT]) and\
             int(element[INIT_Q_POINT]) < int(top_element[END_Q_POINT]) and\
             int(element[END_Q_POINT]) > int(top_element[END_Q_POINT]):
            # Element starts inside reference, and ends after its end.
            # -> Cut the head
            element[INIT_Q_POINT] = str(int(top_element[END_Q_POINT]) + 1)
            element[INIT_S_POINT] = str(int(top_element[END_S_POINT]) + 1)

        elif int(element[INIT_Q_POINT]) > int(top_element[INIT_Q_POINT]) and\
             int(element[END_Q_POINT]) < int(top_element[END_Q_POINT]):
            # Element is embedded
            # -> Delete it
            element[INIT_Q_POINT] = element[END_Q_POINT]
            element[INIT_S_POINT] = element[END_S_POINT]

        element = adjust_score(element, element_length)

        return_list.append(element)

    return return_list 

def cut_elements(list_of_lines, return_list = []):
    """list of lists, list of lists --> (list_of_lists)

    Cut the element of least score by the element of higher score, returning
    the parts left of the elements.
    """
    #TODO Should this be in config? Probably YES
    MIN_LENGTH = 2

    sort_by_score(list_of_lines)

    if len(list_of_lines) == 1 and not return_list:
        #If we got only one match, don't lose time
        return list_of_lines
 
    if len(list_of_lines) > 1:
        ref = list_of_lines.pop(0)
 
        if abs(int(ref[INIT_Q_POINT]) - int(ref[END_Q_POINT])) < MIN_LENGTH:
            #Sequence is too short to be saved. Don't save and rerun
            cut_elements(list_of_lines, return_list = return_list)
        else:
            return_list.append(ref)

        list_of_lines = cut_elements_by_group(list_of_lines, ref)
  
        cut_elements(list_of_lines, return_list = return_list)
           
    return return_list

def clean_embedded(list_of_lines, return_list = []):
    """list of lists, list of lists --> (list_of_lists)

    Deletes all the elements that seems to be embedded or exact match elements,
    returning the rest of the matches
    """

    if len(list_of_lines) > 1:
        # The lines come sorted by insertion point, and are guaranteed to be
        # the same element, the same contig and the same direction

        if int(list_of_lines[1][END_Q_POINT]) <=\
            int(list_of_lines[0][END_Q_POINT]):
            #The after reference line is embedded in the reference, delete it
            list_of_lines.pop(1)
        elif int(list_of_lines[0][INIT_Q_POINT]) ==\
            int(list_of_lines[1][INIT_Q_POINT]):
            # The reference is embedded in the next element, delete it.
            #
            # (First equal in both, but last higher in second element implied
            # on the previous comparison).
            list_of_lines.pop(0)
        else:
            #A new element needs to be worked
            return_list.append(list_of_lines[0])
            list_of_lines.pop(0)

        # Call again recursively with remaining elements
        clean_embedded(list_of_lines, return_list)

    else:
        #Only one element left in the pool, save it and return
        return_list.append(list_of_lines[0])

    return return_list

def load_input_file(i_file):
    """filename --> (list)
    
    Loads and processes a sorted input to cut the overlapped elements
    """
    group = []
 
    ret_list = []

    with open(i_file, "rU") as i_file:
        for line in i_file:
            this_line = line.split()

            if not group:
                group = [this_line]

            else:
                #We got at least one element catched. Now get all elements that
                # can be related to it
                if this_line[SUBJECT_NAME] == group[0][SUBJECT_NAME] and\
                   this_line[DIR] == group[0][DIR] and\
                   this_line[QUERY_NAME] == group[0][QUERY_NAME]:
                    group.append(this_line)
                else:
                   # A different element has been found.
                   # Now clean the group
                   non_embedded = clean_embedded(group, return_list = [])
                   for out_line in cut_elements(non_embedded):
                       ret_list.append(out_line)

                   group = [this_line] #And initialize it again
    #And now the last group of the file
    non_embedded = clean_embedded(group, return_list = [])
    cutted_elements = cut_elements(non_embedded, return_list = [])
    for out_line in cutted_elements:
        ret_list.append(out_line)

    return ret_list

def sort_by_score(list_of_elements):
    """list of lists -> None

    Takes a list and sort in place it by the score. In the case of tie,
    sort it by identity %.

    The line type is:

    1211.0 100.0 query_name 1 1027 + subject_name 237 1263

    where (zero indexed):
    
     [0] is the score
     [1] is the similarity
    """

    gets = operator.itemgetter(SCORE, IDENTITY)

    for line in list_of_elements:
        line[SCORE] = float(line[SCORE])
        line[IDENTITY] = float(line[IDENTITY])

    list_of_elements.sort(key=gets, reverse=True)

    for line in list_of_elements:
        line[SCORE] = str(line[SCORE])
        line[IDENTITY] = str(line[IDENTITY])

    return True

if __name__ == "__main__":
    try:
        i_file = sys.argv[1]
    except IndexError:
        print '''
        Utilizacion:
        {0} input
        e.g.
        
           {0} input.txt
           {0} input.txt > output.txt
        '''.format(__file__)

        sys.exit()

    non_embedded = load_input_file(i_file)
    for x in non_embedded:
        print " ".join(x)

