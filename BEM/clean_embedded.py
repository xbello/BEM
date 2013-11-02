#!/usr/bin/env python
import sys

"""This script simply takes a sorted output and deletes all elements that seems
to be embedded or equal to another of the same class.
"""

def clean_embedded(list_of_lines, return_list = []):
    """list of lists, list of lists --> (list_of_lists)

    Deletes all the elements that seems to be embedded or exact match elements,
    returning the rest of the matches
    """
    if len(list_of_lines) > 1:
        # The lines come sorted by insertion point, and are guaranteed to be
        # the same element, the same contig and the same direction

        if int(list_of_lines[1][6]) <= int(list_of_lines[0][6]):
            #The after reference line is embedded in the reference, delete it
            list_of_lines.pop(1)
        elif int(list_of_lines[0][5]) == int(list_of_lines[1][5]):
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

def cut_elements(list_of_lines):
   """list of lists --> (list_of_lists)

   Cut the element of least score by the element of higher score, returning
   the parts left of the elements.
   """
   if len(list_of_lines) > 1:
       for element in list_of_lines:
           # TODO: 
           # If cutted element is less than 1 bp, pop it, and don't advance
           # Otherwise, keep cutting and advancing
           
           pass
   else:
       return list_of_lines


def load_input_file(i_file):
    """filename --> (None)
    
    Loads and processes a sorted input to clean the embedded elements
    """
    group = []

    with open(i_file, "rU") as i_file:
        for line in i_file:
            this_line = line.split()

            if not group:
                group = [this_line]

            else:
                #We got at least one element catched. Now get all elements that
                # can be related to it
                if this_line[4] == group[0][4] and\
                   this_line[8] == group[0][8] and\
                   this_line[9] == group[0][9]:
                    group.append(this_line)
                else:
                   #Now clean the group
                   for out_line in clean_embedded(group, return_list = []):
                       print " ".join(out_line)
                   group = [this_line] #And initialize it again
                   

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

