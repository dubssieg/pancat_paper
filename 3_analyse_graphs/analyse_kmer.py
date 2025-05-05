#!/usr/bin/env python3
from sys import argv
from json import dump
from subprocess import check_output
from typing import Any

# file should be a .fasta file (the reference genome)
fasta_file: str = argv[1]
# change the sampling to change the number of windows over the genome
sampling: int = 200
ksize: int = 9

kmer_results: dict[str, Any] = {
    'reference_size': 0,
    'unique_kmers': [0] * sampling,
    'ratios': 0,
    'ksize': ksize
}


x: str = check_output(
    f"awk '/^>/ {{if (seqlen){{print seqlen}}; print ;seqlen=0;next; }} {{ seqlen += length($0)}}END{{print seqlen}}' {fasta_file}", shell=True
)
reference_size: int = int(str(x).split('\\n')[1])
kmer_results['reference_size'] = reference_size
ratios: float = sampling/reference_size
kmer_results['ratios'] = ratios

kmers: list = [set() for _ in range(sampling)]
with open(fasta_file, 'r', encoding='utf-8') as f:
    # Read the data
    for l in f:
        if l.startswith('>'):
            continue
        else:
            sequence: str = l.strip()
            for i in range(reference_size-ksize):
                kmers[int(int(i)*ratios)].add(sequence[i:i+ksize])

for i in range(sampling):
    kmer_results['unique_kmers'][i] = len(kmers[i])

# Save the results
with open(f'{fasta_file}.json', 'w', encoding='utf-8') as f:
    dump(kmer_results, f)
