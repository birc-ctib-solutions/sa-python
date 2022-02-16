import sys
import argparse
from dataclasses import dataclass
from sais import sais
from fasta import read_fasta
from fastq import scan_reads
from sam import ssam_record
from sa_bsearch import sa_bsearch


@dataclass
class ChromosomeSA:
    seq: str
    sa: list[int]


def main():
    argparser = argparse.ArgumentParser(
        description="Exact matching using a suffix array")
    argparser.add_argument("genome", type=argparse.FileType('r'))
    argparser.add_argument("reads", type=argparse.FileType('r'))
    args = argparser.parse_args()

    genome: dict[str, ChromosomeSA] = {
        name: ChromosomeSA(seq, sais(seq)) for name, seq in read_fasta(args.genome).items()
    }

    for read_name, read_seq in scan_reads(args.reads):
        for chr_name, chrom in genome.items():
            for i in sa_bsearch(read_seq, chrom.seq, chrom.sa):
                ssam_record(sys.stdout,
                            read_name, chr_name,
                            i, f"{len(read_seq)}M",
                            read_seq)


if __name__ == '__main__':
    main()
