import argparse
import ConfigParser
import os
from multiprocessing import Pool, Process, cpu_count

import utils

CORES = cpu_count()
config = ConfigParser.RawConfigParser()
config.read("config.cfg")
output_path = config.get("paths", "output_db")

def blast(query, subject, evalue, penalty, reward, gapopen, gapextend):
    #Run the blast
    p = Process(target=utils.blast, args=(query,))

def format_db(subject):
    #Format each db
    #assert subject exist
    for core in CORES:
        utils.format_database(
            os.path.join(output_path, core, subject), db_type)

    return True

def span_cores(subject):
    #Span the subject across CPUs available
    assert os.path.isfile(subject), "File doesn't exist {0}".format(subject)
    utils.multicore(subject, CORES)
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs a blast.")
    parser.add_argument("--query", dest="query", required=True)
    parser.add_argument("--subject", dest="subject", required=True)
    parser.add_argument("--evalue", dest="evalue",
        help="e-value expressed as the power of ten, being 5 = 10^-5")
    parser.add_argument("--penalty", dest="penalty")
    parser.add_argument("--reward", dest="reward")
    parser.add_argument("--gapopen", dest="gapopen")
    parser.add_argument("--gapextend", dest="gapextend")
 
    args = parser.parse_args()

    span_cores(args.subject)
    format_db(args.subject)
