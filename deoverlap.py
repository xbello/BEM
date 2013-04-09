#!/usr/bin/env python
import operator
import sys

"""This script simply takes a sorted output and cut the elements if two
sequences seems to be ocupying the same spot.
"""

def adjust_score(element, old_length):
    """list, int -> (list)

    Adjust the new score of a post-cut element. We are going to assume that 
    every base of the match provides the same amount of score.
    """
    INIT_Q_POINT = 3
    END_Q_POINT = 4

    old_score = float(element[0])
    
    score_per_base = 0.0
    if old_score > 0:
        score_per_base = old_score / old_length

    new_length = abs(int(element[END_Q_POINT]) - \
                 int(element[INIT_Q_POINT]))

    element[0] = "{0:.1f}".format(new_length * score_per_base)

    return element
   

def cut_elements(list_of_lines, return_list = []):
    """list of lists, list of lists --> (list_of_lists)

    Cut the element of least score by the element of higher score, returning
    the parts left of the elements.
    """

    INIT_Q_POINT = 3
    END_Q_POINT = 4
    INIT_S_POINT = 7
    END_S_POINT = 8
    MIN_LENGTH = 2

    sort_by_score(list_of_lines)
 
    if len(list_of_lines) > 1:
        ref = list_of_lines.pop(0)
 
        if abs(int(ref[INIT_Q_POINT]) - int(ref[END_Q_POINT])) < MIN_LENGTH:
            #Sequence is too short to be saved. Don't save and rerun
            cut_elements(list_of_lines, return_list)
        else:
            return_list.append(ref)
 
        for element in list_of_lines:
            # First we save the element original length to readjust the score
            # further on
            element_length = abs(int(element[END_Q_POINT]) - \
                int(element[INIT_Q_POINT]))

            if int(element[INIT_Q_POINT]) < int(ref[INIT_Q_POINT]) and\
               int(element[END_Q_POINT]) > int(ref[INIT_Q_POINT]) and\
               int(element[END_Q_POINT]) < int(ref[END_Q_POINT]):
                # Element start before reference, overlaps with it, ends before
                # -> Cut the tail
                element[END_Q_POINT] = str(int(ref[INIT_Q_POINT]) - 1)
                element[END_S_POINT] = str(int(ref[INIT_S_POINT]) - 1)
                
 
            elif int(element[INIT_Q_POINT]) > int(ref[INIT_Q_POINT]) and\
                 int(element[INIT_Q_POINT]) < int(ref[END_Q_POINT]) and\
                 int(element[END_Q_POINT]) > int(ref[END_Q_POINT]):
                # Element starts inside reference, and ends after its end.
                # -> Cut the head
                element[INIT_Q_POINT] = str(int(ref[END_Q_POINT]) + 1)
                element[INIT_S_POINT] = str(int(ref[END_S_POINT]) + 1)
 
            elif int(element[INIT_Q_POINT]) > int(ref[INIT_Q_POINT]) and\
                 int(element[END_Q_POINT]) < int(ref[END_Q_POINT]):
                # Element is embedded
                # -> Delete it
                element[INIT_Q_POINT] = element[END_Q_POINT]
                element[INIT_S_POINT] = element[END_S_POINT]
 
            element = adjust_score(element, element_length)
 
        cut_elements(list_of_lines, return_list)
           #Cut all elements by first element
           ##Elements too short (<= 1) should be removed
           #Pop first element, preserve all others
           #recursive the function with remaining elements
           
    return return_list

def clean_embedded(list_of_lines, return_list = []):
    """list of lists, list of lists --> (list_of_lists)

    Deletes all the elements that seems to be embedded or exact match elements,
    returning the rest of the matches
    """
    INIT_Q_POINT = 3
    END_Q_POINT = 4

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
    """filename --> (None)
    
    Loads and processes a sorted input to cut the overlapped elements
    """
    group = []
    CROM_NAME = 2
    EL_DIR = 5
    EL_NAME = 6

    with open(i_file, "rU") as i_file:
        for line in i_file:
            this_line = line.split()

            if not group:
                group = [this_line]

            else:
                #We got at least one element catched. Now get all elements that
                # can be related to it
                if this_line[CROM_NAME] == group[0][CROM_NAME] and\
                   this_line[EL_DIR] == group[0][EL_DIR] and\
                   this_line[EL_NAME] == group[0][EL_NAME]:
                    group.append(this_line)
                else:
                   #Now clean the group
                   for out_line in clean_embedded(group, return_list = []):
                       print " ".join(out_line)
                   group = [this_line] #And initialize it again
        #And now the last group of the file
        for out_line in clean_embedded(group, return_list = []):
            print " ".join(out_line)

def sort_by_score(list_of_elements):
    """list -> None

    Takes a list and sort in place it by the score. In the case of tie,
    sort it by identity %.

    The line type is:

    1211.0 100.0 query_name 1 1027 + subject_name 237 1263

    where (zero indexed):
    
     [0] is the score
     [1] is the similarity
    """

    gets = operator.itemgetter(0, 1)

    for line in list_of_elements:
        line[0] = float(line[0])
        line[1] = float(line[1])

    list_of_elements.sort(key=gets, reverse=True)

    for line in list_of_elements:
        line[0] = str(line[0])
        line[1] = str(line[1])

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

    load_input_file(i_file)

