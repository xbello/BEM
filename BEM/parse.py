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
            "identity": round(float(data[2]), 2),
            "length": int(data[3]),
            "n_match": int(data[4]),
            "query_start": int(data[6]),
            "query_end": int(data[7]),
            "subject_start": int(data[8]),
            "subject_end": int(data[9]),
            "e_val": round(float(data[10]), 3),
            "score": round(float(data[11]), 2)}
