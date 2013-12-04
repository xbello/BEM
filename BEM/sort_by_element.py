#!/usr/bin/env python

"""Sort a crude output from BLAST.

That sorted output allows the reconstruction of the longest elements
possible. For that we aim to group the elements by chromosome, then for
element, then for direction, then for insertion point and then for score.

After that sorting, all the elements of a chromosome (contig) are sequentially
positioned, and thus we can join/cut/delete all elements that can be joined,
are overlapped or directly embedded.

The line type is:

1211.0 100.0 query_name 1 1027 + subject_name 237 1263

Where (zero indexed):

 [2] is the element name
 [6] is the contig/genome name
 [5] is the direction
 [3] is the insertion point
 [0] is the score

"""

import operator
import sys

from defs import *


def sort_file(input_file):
    """Sort the lines on input_file. Returns a list of lines."""

    gets = operator.itemgetter(
        SUBJECT_NAME, QUERY_NAME, DIR, INIT_Q_POINT, SCORE)

    lines = []

    with open(input_file, "rU") as in_file:
        for line in in_file:
            lines.append(line.strip().split())

    lines.sort(key=gets)

    return lines

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

    for line in sort_file(i_file):
        print " ".join(line)
