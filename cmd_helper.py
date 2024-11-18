#this file contains linux comand line functions
import argparse

def defineArguments(parser):
    parser.add_argument("reference", type=str, help="FASTA datoteka s referencom")
    parser.add_argument("num_reads", type=int, help="Broj očitanja koja će se generirati")
    parser.add_argument("output_fastq", type=str, help="Izlazna FASTQ datoteka za generirana očitanja")
    parser.add_argument("--substitution_rate", type=float, default=0.01, help="Postotak zamjena (default: 0.01)")
    parser.add_argument("--insertion_rate", type=float, default=0.005, help="Postotak umetanja (default: 0.005)")
    parser.add_argument("--deletion_rate", type=float, default=0.005, help="Postotak brisanja (default: 0.005)")
    parser.add_argument("--mean_length", type=int, default=150, help="Prosječna duljina očitanja (default: 150)")
    parser.add_argument("--stddev_length", type=int, default=15, help="Standardna devijacija duljine očitanja (default: 15)")
    