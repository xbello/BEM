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

    HSP_keys = ["query", "subject", "identity", "length", "n_mismatch",
        "n_gaps", "query_start", "query_end", "subject_start", "subject_end",
        "e_val", "score"]

    with open(blast_output_file, "r") as blast_output:
        for line in blast_output:
            
            data = line.strip().split("\t")
            HSP = dict.fromkeys(HSP_keys)

            for fl in ["identity", "e_val", "score"]:
                HSP[fl] = float(data[HSP_keys.index(fl)])
            for integer in ["length", "n_mismatch", "n_gaps", "query_start",
                "query_start", "query_end", "subject_start", "subject_end"]:
                HSP[integer] = int(data[HSP_keys.index(integer)])
            for strin in ["query", "subject"]:
                HSP[strin] = data[HSP_keys.index(strin)]
                

            yield HSP

def write_parsed(file_handle, HSP_dict):
    '''From a dict yielded from blast_table_consumer, write a line in the 
    file_handle'''
    header = ["score", "identity", "query", "query_start", "query_end",
        "direction", "subject", "subject_start", "subject_end"]

    HSP_dict["direction"] = "+"
    if HSP_dict["query_start"] < HSP_dict["query_end"]:
        HSP_dict["direction"] == "C"

    for column in header:
        file_handle.write(str(HSP_dict[column]) + " ")

    file_handle.write("\n")

    return True

if __name__ == "__main__":
    f_h = open("test.blout", "w")
    for HSP in blast_table_consumer("tests/output.blast"):
        write_parsed(f_h, HSP)
