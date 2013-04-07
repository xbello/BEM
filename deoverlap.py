#!/usr/bin/env python
import operator
import sys

"""This script simply takes a sorted output and cut the elements if two
sequences seems to be ocupying the same spot.
"""

def cut_elements(list_of_lines, return_list = []):
   """list of lists, list of lists --> (list_of_lists)

   Cut the element of least score by the element of higher score, returning
   the parts left of the elements.
   """

   INIT_POINT = 3
   END_POINT = 4

   sort_by_score(list_of_lines)
   #TODO: Test this shit

   if len(list_of_lines) > 1:
       ref = list_of_lines.pop(0)
       return_list.append(ref)

       for element in list_of_lines:
           if int(element[INIT_POINT]) < int(ref[INIT_POINT]) and\
              int(element[END_POINT]) > int(ref[INIT_POINT]) and\
              int(element[END_POINT]) < int(ref[END_POINT]):
               # Element start before reference, overlaps with it, ends before
               # -> Cut the tail
               element[END_POINT] = str(int(ref[INIT_POINT]) - 1)

           elif int(element[INIT_POINT]) > int(ref[INIT_POINT]) and\
                int(element[INIT_POINT]) < int(ref[END_POINT]) and\
                int(element[END_POINT]) > int(ref[END_POINT]):
               # Element starts inside reference, and ends after its end.
               # -> Cut the head
               element[INIT_POINT] = str(int(ref[END_POINT]) + 1)

           elif int(element[INIT_POINT]) > int(ref[INIT_POINT]) and\
                int(element[END_POINT]) < int(ref[END_POINT]):
               # Element is embedded
               # -> Delete it
               element[INIT_POINT] = element[END_POINT]

       cut_elements(list_of_lines, return_list)
           #Cut all elements by first element
           ##Elements too short (<= 1) should be removed
           #Pop first element, preserve all others
           #recursive the function with remaining elements
           
   else:
       return list_of_lines

def clean_embedded(list_of_lines, return_list = []):
    """list of lists, list of lists --> (list_of_lists)

    Deletes all the elements that seems to be embedded or exact match elements,
    returning the rest of the matches
    """
    INIT_POINT = 3
    END_POINT = 4

    if len(list_of_lines) > 1:
        # The lines come sorted by insertion point, and are guaranteed to be
        # the same element, the same contig and the same direction

        if int(list_of_lines[1][END_POINT]) <=\
            int(list_of_lines[0][END_POINT]):
            #The after reference line is embedded in the reference, delete it
            list_of_lines.pop(1)
        elif int(list_of_lines[0][INIT_POINT]) ==\
            int(list_of_lines[1][INIT_POINT]):
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

