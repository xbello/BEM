#!/usr/bin/env/ python
"""Proxy for BLASTing sequences."""

import argparse
import ConfigParser
import os
from multiprocessing import cpu_count
from subprocess import Popen, PIPE

import config
import utils


def blastn(query, subject, config):
    """Launch a blastn."""
    num_threads = cpu_count()

    binary = os.path.join(
        config.get("binaries", "blast"),
        config.get("binaries", "blastn"))

    output_db = config.get("paths", "output_db")
    output_blast = config.get("paths", "output_blast")

    input_path = config.get("paths", "input_path")

    # Don't be too greedy, and lift one core to the user if there're many
    if num_threads > 1:
        num_threads -= 1

    command = [
        binary,
        "-query", os.path.join(input_path, query),
        "-subject", subject,
        "-db", os.path.join(output_db, subject),
        "-outfmt", "6"]

    # TODO: add here all blast options

    p = Popen(command)

    p.communicate()


def format_db(subject, db_type):
    utils.format_database(subject, db_type, config)

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs a blast.")
    parser.add_argument("--query", dest="query", required=True)
    parser.add_argument("--subject", dest="subject", required=True)
    parser.add_argument("--strategy", dest="strategy", default="blastn")
    parser.add_argument("--config", dest="config_file")

    args = parser.parse_args()

    config_values = config.get_config_file(config)

    if args.strategy == "blastn":
        format_db(args.subject, "nucl")
        blastn(args.query,
               args.subject,
               config)

    elif args.strategy == "tblastn":
        format_db(args.subject, "prot")

