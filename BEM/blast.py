#!/usr/bin/env/ python
"""Proxy for BLASTing sequences."""

import argparse
import os
from multiprocessing import Pool, cpu_count
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile

from Bio import SeqIO


def blastn(query, subject, conf):
    """Launch a blastn."""

    binary = os.path.join(
        conf.get("binaries", "blast"),
        conf.get("binaries", "blastn"))

    output_db = conf.get("paths", "output_db")
    input_path = conf.get("paths", "input_path")

    command = [
        binary,
        "-query", os.path.join(input_path, query),
        "-db", os.path.join(output_db, subject),
        "-outfmt", "6",
        "-task", conf.get("blastn", "task"),
        "-evalue", conf.get("blastn", "evalue"),
        "-word_size", conf.get("blastn", "word"),
        "-penalty", conf.get("blastn", "penalty"),
        "-reward", conf.get("blastn", "reward"),
        "-gapopen", conf.get("blastn", "gapopen"),
        "-gapextend", conf.get("blastn", "gapextend")]

    return run_command(command)


def format_db(fasta_src, db_type, conf):
    """Return the output after formating a database to use with NCBI BLAST.

    db_type is ``nucl`` or ``prot``.

    """

    assert db_type in ["nucl", "prot"]

    binary = conf.get("binaries", "makeblastdb")
    binary_path = conf.get("binaries", "blast")
    output_path = conf.get("paths", "output_db")

    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    input_path = conf.get("paths", "input_path")

    command = [
        os.path.join(binary_path, binary),
        "-in", os.path.join(input_path, fasta_src),
        "-out", os.path.join(output_path, fasta_src),
        "-dbtype", db_type]

    return run_command(command)


def run_command(command):
    """Return the output of a command after running it under subprocess."""

    sub = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = sub.communicate()

    if stderr:
        # TODO: Some programs throws common messages through stderr.
        raise IOError(stderr)

    return stdout


def split_query(query_file, n=100):
    """Return a generator of Tempfiles with n seqs each."""

    pack = []
    for record in SeqIO.parse(query_file, "fasta"):
        pack.append(record)

        if len(pack) == n:
            # Enough sequences has been collected, pack and yield
            yield join_pack(pack)
            pack = []

    # Yield last pack if any
    if pack:
        yield join_pack(pack)


def join_pack(pack):
    """Yield a pack of sequences."""

    new_fasta = NamedTemporaryFile(delete=False)

    SeqIO.write(pack, new_fasta, "fasta")
    new_fasta.seek(0)

    return new_fasta


if __name__ == "__main__":
    import config

    parser = argparse.ArgumentParser(description="Runs a blast.")
    parser.add_argument("--query", dest="query", required=True)
    parser.add_argument("--subject", dest="subject", required=True)
    parser.add_argument("--strategy", dest="strategy", default="blastn")
    parser.add_argument("--config", dest="config_file")

    args = parser.parse_args()

    config_values = config.get_config_file(args.config_file)

    # Use all available CPUs
    pool = Pool(cpu_count())

    if args.strategy == "blastn":
        format_db(args.subject, "nucl", config_values)
        # Lower the nice value
        os.nice(5)
        # Unset the file_source
        config_values.set("paths", "input_path", "")
        for file_handler in split_query(args.query):
            blastout = blastn(
                file_handler.name, args.subject, config_values)
            # Delete the intermediary Tempfile
            os.unlink(file_handler.name)

    elif args.strategy == "tblastn":
        format_db(args.subject, "prot", config_values)
