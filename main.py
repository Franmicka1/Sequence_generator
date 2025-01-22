import random
import argparse
import cmd_helper
import subprocess
import numpy as np
import json

class ReadSimulator:
    def __init__(self, args):
        self.reference = args.reference
        self.num_reads = args.num_reads
        self.output_fastq = args.output_fastq
        self.technology = args.technology
        self.num_chim_reads = args.num_chim_reads
        self.initialize_technology_args()
        self.override_techonlogy_args(args)
    
    def initialize_technology_args(self):
        file_name = 'technologies.json'
        with open(file_name, 'r') as file:
            json_data = json.load(file)
        for key,value in json_data['technologies'][self.technology].items():
            setattr(self, key, value)
                
    
    def override_techonlogy_args(self, args):
        if args.substitution_rate:
            self.error_profile['substitution_rate'] = args.substitution_rate
        if args.insertion_rate:
            self.error_profile['insertion_rate'] = args.insertion_rate
        if args.deletion_rate:
            self.error_profile['deletion_rate'] = args.deletion_rate
        if args.read_mean:
            self.read_mean = args.read_mean
        if args.read_stddev:
            self.read_stddev = args.read_stddev
        
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

    def get_read_length(self):
        distribution_function = getattr(np.random, self.read_length_distribution)
        
        if self.read_length_distribution == 'normal':
            return int(distribution_function(self.read_mean, self.read_stddev))
        elif self.read_length_distribution == 'lognormal':
            return int(distribution_function(self.read_mean, self.read_stddev))   
        elif self.read_length_distribution == 'exponential':
            return int(distribution_function(1/self.read_mean))
        else:
            return max(1, int(np.random.normal(1000, 100)))

    def resolve_chim_reads(self, reads):
        while len(reads) > self.num_reads:
            combine_indexes = random.sample(range(len(reads)), 2)
            combine_indexes.sort(reverse=True)
            read0 = reads.pop(combine_indexes[0])
            read1 = reads.pop(combine_indexes[1])
            new_read = read0 + read1
            reads.append(new_read)

    def reverse_complement(self, read):
        complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        reverse_complement_chance = 0.5
        if (random.random() > reverse_complement_chance):
            return ''.join(complement[base] for base in reversed(read))

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
        total_reads = int(self.num_reads * (1+self.num_chim_reads))
        for _ in range(total_reads):
            chrom = random.choice(list(sequences.keys()))
            seq = sequences[chrom]
            read_length = self.get_read_length()
            start = random.randint(0, len(seq) - read_length)
            read = seq[start:start + read_length]
            self.reverse_complement(read)
            reads.append(read)
        self.resolve_chim_reads(reads)  
        
        for index, read in enumerate(reads):
            read_with_errors = self.introduce_errors(read)
            reads[index] = read_with_errors
            
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
    simulator = ReadSimulator(args)
    sequences = simulator.load_reference()
    reads = simulator.generate_reads(sequences)
    simulator.save_reads(reads)
  
if __name__ == "__main__":
    main()