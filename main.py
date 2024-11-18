import random
import argparse
import cmd_helper
import subprocess
import numpy as np

class ReadSimulator:
    def __init__(self, reference, num_reads, substitution_rate, insertion_rate, deletion_rate, mean_length, stddev_length, output_fastq):
        self.reference = reference
        self.num_reads = num_reads
        self.substitution_rate = substitution_rate
        self.insertion_rate = insertion_rate
        self.deletion_rate = deletion_rate
        self.mean_length = mean_length
        self.stddev_length = stddev_length
        self.output_fastq = output_fastq
        self.error_profile = {
        'substitution': self.substitution_rate,
        'insertion': self.insertion_rate,
        'deletion': self.deletion_rate
        }

    def load_reference(self):
        sequences = {}
        with open(self.reference, 'r') as f:
            current_seq = ""
            current_chrom = None
            for line in f:
                if line.startswith(">"):
                    if current_chrom:
                        sequences[current_chrom] = current_seq
                    current_chrom = line[1:].strip()
                    current_seq = ""
                else:
                    current_seq += line.strip()
            if current_chrom:
                sequences[current_chrom] = current_seq
        return sequences

    def introduce_errors(self, seq):
        error_seq = []
        for base in seq:
            r = random.random()
            if r < self.error_profile['substitution']:
                bases = ['A', 'T', 'C', 'G']
                bases.remove(base)
                error_seq.append(random.choice(bases))

            elif r < self.error_profile['substitution'] + self.error_profile['insertion']:
                error_seq.append(base)
                error_seq.append(random.choice(['A', 'T', 'C', 'G']))

            elif r < self.error_profile['substitution'] + self.error_profile['insertion'] + self.error_profile['deletion']:
                continue
            else:
                error_seq.append(base)
        return "".join(error_seq)

    def generate_reads(self, sequences):
        reads = []
        for _ in range(self.num_reads):
            chrom = random.choice(list(sequences.keys()))
            seq = sequences[chrom]
            read_length = max(1, int(np.random.normal(self.mean_length, self.stddev_length)))
            start = random.randint(0, len(seq) - read_length)
            read = seq[start:start + read_length]
            read_with_errors = self.introduce_errors(read)
            reads.append(read_with_errors)
        return reads
    
    def save_reads(self, reads):
        with open(self.output_fastq, 'w') as f:
            for i, read in enumerate(reads):
                f.write(f">read{i}\n")
                f.write(f"{read}\n")
        print(f"Generirano {self.num_reads} očitanja u {self.output_fastq}.")

def main():
    parser = argparse.ArgumentParser(description="Simulacija sekvenciranja s pogreškama i testiranje pomoću Minimap2")
    cmd_helper.defineArguments(parser)
    
    args = parser.parse_args()
    simulator = ReadSimulator(
        reference=args.reference,
        num_reads = args.num_reads,
        substitution_rate=args.substitution_rate,
        insertion_rate=args.insertion_rate,
        deletion_rate=args.deletion_rate,
        mean_length=args.mean_length,
        stddev_length=args.stddev_length,
        output_fastq = args.output_fastq
    )
    sequences = simulator.load_reference()
    reads = simulator.generate_reads(sequences)
    simulator.save_reads(reads)
  
if __name__ == "__main__":
    main()