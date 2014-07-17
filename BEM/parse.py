"""Deal with the returning format for NCBI-BLAST."""


BLAST_HSP_KEYS = [
    "query", "subject", "identity", "length", "n_match",
    "n_gaps", "query_start", "query_end", "subject_start", "subject_end",
    "e_val", "score"]


def blast_tab(blast_output):
    """Return the HSPs from a blast output with tab format."""

    for hsp in blast_output.splitlines():
        data = hsp.split()

        yield {
            "query": data[0],
            "subject": data[1],
            "identity": data[2],
            "length": data[3],
            "n_match": data[4],
            "query_start": data[6],
            "query_end": data[7],
            "subject_start": data[8],
            "subject_end": data[9],
            "e_val": data[10],
            "score": data[11]}
