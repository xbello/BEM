
def select_blaster_keys(splitted_line):
    """list -> (dict)
    
    Given a line of tabular output, return the header keys of the blaster.
    This is a line from WU-BLAST:
     "Query    Subject 1.4e-11 1       71.62   437     520     307     307     172     59.04   59.04   18      18      21      23      -1      3651    3150    +1      396     892"
    
    22 columns divided by \t

    This is a line from BLAST:
     "Query       Subject      100.00  1027    0       0       1       1027    237     1263    0.0     1211"

     12 columns divided by \t
    """

    WUBLAST_HSP_KEYS = HSP_keys = ["query", "subject", "e_val", "n_scores",
        "score_norm", "score", "length", "idents", "matchs", "n_mismatch",
        "identity", "pc_pos", "n_gaps", "gap_len", "subject_gaps",
        "subject_gap_len", "query_frame", "query_start", "query_end",
        "subject_frame", "subject_start", "subject_end"]

    BLAST_HSP_KEYS = ["query", "subject", "identity", "length", "n_mismatch",
        "n_gaps", "query_start", "query_end", "subject_start", "subject_end",
        "e_val", "score"]

    if len(splitted_line) == 22:
        return WUBLAST_HSP_KEYS
    elif len(splitted_line) == 12:
        return BLAST_HSP_KEYS
    else:
        raise Exception, "BLAST output cannot be determined"

def blast_table_consumer(blast_output_file):
    '''Consume a blast file, yielding a dict entry:
    HSP = {"query": str,
           "subject": str,
           "identity": float,
           "length": int,
           "n_mismatch": int,
           "n_gaps": int,
           "query_start": int,
           "query_end": int,
           "subject_start": int,
           "subject_end":int,
           "e_val": float,
           "score": float}

    The blast_output_file must come ready to be opened directly.'''

    with open(blast_output_file, "r") as blast_output:
        for line in blast_output:
            
            data = line.strip().split("\t")

            HSP_keys = select_blaster_keys(data)
            HSP = {}

            for fl in ["identity", "e_val", "score"]:
                HSP[fl] = float(data[HSP_keys.index(fl)])
            for integer in ["length", "n_mismatch", "n_gaps", "query_start",
                "query_start", "query_end", "subject_start", "subject_end"]:
                HSP[integer] = int(data[HSP_keys.index(integer)])
            for strin in ["query", "subject"]:
                HSP[strin] = data[HSP_keys.index(strin)]

            yield HSP

def write_parsed(HSP_dict):
    '''From a dict yielded from blast_table_consumer, write a line to the 
    stdout'''
    header = ["score", "identity", "query", "query_start", "query_end",
        "direction", "subject", "subject_start", "subject_end"]

    HSP_dict["direction"] = "+"
    for target in ["subject", "query"]:
        if HSP_dict["{0}_start".format(target)] >\
           HSP_dict["{0}_end".format(target)]:
            HSP_dict["direction"] = "C"
            #Swap the start and ending points
            HSP_hold = HSP_dict["{0}_start".format(target)]
            HSP_dict["{0}_start".format(target)] =\
                HSP_dict["{0}_end".format(target)]
            HSP_dict["{0}_end".format(target)] = HSP_hold

    line = []
    for column in header:
        line.append(str(HSP_dict[column]))

    return " ".join(line)

if __name__ == "__main__":
    import sys

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

    for HSP in blast_table_consumer(i_file):
        print write_parsed(HSP)
