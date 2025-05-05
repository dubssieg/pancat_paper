#!/usr/bin/env python3
from sys import argv
from json import dump
from subprocess import check_output
from typing import Any

# checks for segmental duplication bases
# file should be a .bed file. For use with BISER, we must change indexes.
file_name: str = argv[1]
fasta_file: str = argv[2]
chrom_name: str = argv[3]
# change the sampling to change the number of windows over the genome
sampling: int = 200

sd_results: dict[str, Any] = {
    'reference_size': 0,
    'segmental_duplications': [0] * sampling,
    'ratios': 0
}


x: str = check_output(
    f"awk '/^>/ {{if (seqlen){{print seqlen}}; print ;seqlen=0;next; }} {{ seqlen += length($0)}}END{{print seqlen}}' {fasta_file}", shell=True
)
reference_size: int = int(str(x).split('\\n')[1])

sd_results['reference_size'] = reference_size
ratios: float = sampling/reference_size
window = reference_size/sampling
sd_results['ratios'] = ratios

sd_bitvector = [0] * reference_size

with open(file_name, 'r', encoding='utf-8') as f:
    # Read the data
    for l in f:
        if l.strip().split('\t')[0] == chrom_name:
            start, end = int(l.strip().split('\t')[1]), int(
                l.strip().split('\t')[2])
            for posx in range(start, end):
                sd_bitvector[posx] = 1

# Count number of bases in each window
for i in range(sampling):
    sd_results['segmental_duplications'][i] = sum(
        sd_bitvector[int(i*window):int((i+1)*window)])

# Save the results
with open(f'{file_name}.json', 'w', encoding='utf-8') as f:
    dump(sd_results, f)
