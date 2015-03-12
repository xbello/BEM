"""Yield groups of fasta sequences from a fasta file."""
from tempfile import NamedTemporaryFile
from Bio import SeqIO


def files(fasta_file, group_size):
    """Return a generator with files and each file with group_size Seqs."""
    return group(fasta_file, group_size)


def group(fasta_file, group_size):
    """Yield groups of Bio.Seqs from the fasta_gen of size group_size."""

    fasta_gen = SeqIO.parse(fasta_file, "fasta")

    group = []
    while fasta_gen:
        try:
            this_seq = next(fasta_gen)
            group.append(this_seq)
        except StopIteration:
            if group:
                # Never yield an empty group
                yield group
            raise StopIteration

        if len(group) == group_size:
            yield group
            group = []


def save_bioseqs(seq_group):
    """Return a TempFile with a group of sequences."""

    tmp_file = NamedTemporaryFile("w+")
    SeqIO.write(seq_group, tmp_file, "fasta", )
    tmp_file.seek(0)

    return tmp_file
