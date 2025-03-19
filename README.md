# Sequence_generator 
Run script with thchnology selection:
python main.py reference.fasta 10000 output.fastq --technology Illumina

Where:
reference.fasta - represents reference genome.

output.fastq - represents output file to which reads will be saved.

10000 - defines number of generates sequences.

--technology Illumina - defines used technology (options: Illumina, PacBio, Nanopore).

Run unittests with: python -m tests._testname_
