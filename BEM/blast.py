import argparse
import ConfigParser
import os
from multiprocessing import Pool, Process, cpu_count

import utils

CORES = cpu_count()
config = ConfigParser.RawConfigParser()
config.read("config.cfg")
output_path = config.get("paths", "output_db")

def blast(query, subject, evalue, word, penalty, reward, gapopen, gapextend):
    """This is a docstring"""
    p = Process(target=utils.blastn, args=(query, subject, evalue, word, 
        penalty, reward, gapopen, gapextend,))
    p.start()
    p.join()

def format_db(subject, db_type):
    #Format each db
    #assert subject exist
    for core in range(CORES):
        utils.format_database(subject, db_type, config)

    return True

def span_cores(subject):
    #Span the subject across CPUs available
    assert os.path.isfile(subject), "File doesn't exist {0}".format(subject)
    subjects = utils.multicore(subject, config, CORES)
    return subjects

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs a blast.")
    parser.add_argument("--query", dest="query", required=True)
    parser.add_argument("--subject", dest="subject", required=True)
    parser.add_argument("--dbtype", dest="dbtype", default="nucl")
    parser.add_argument("--evalue", dest="evalue", default="5",
        help="e-value expressed as the power of ten, being 5 = 10^-5")
    parser.add_argument("--word", dest="word", default=11)
    parser.add_argument("--penalty", dest="penalty", type=int, default=-5)
    parser.add_argument("--reward", dest="reward", type=int, default=5)
    parser.add_argument("--gapopen", dest="gapopen", type=int, default=10)
    parser.add_argument("--gapextend", dest="gapextend", type=int, default=10)
 
    args = parser.parse_args()

    spanned_subjects = span_cores(args.subject)
    #format_db(args.subject, args.dbtype)
    for subject in spanned_subjects:
        format_db(subject, args.dbtype)
        #blast(args.query, subject, args.evalue, args.penalty,
        #    args.reward, args.gapopen, args.gapextend)
