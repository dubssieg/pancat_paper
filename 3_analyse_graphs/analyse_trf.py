#!/usr/bin/env python3
from sys import argv
from json import dump
from subprocess import check_output
from typing import Any

# file should be a .bed file issued from the conversion of the .dat TRF file
file_name: str = argv[1]
fasta_file: str = argv[2]
# change the sampling to change the number of windows over the genome
sampling: int = 200

trf_results: dict[str, Any] = {
    'reference_size': 0,
    'tandem_repeats': [0] * sampling,
    'ratios': 0
}


x: str = check_output(
    f"awk '/^>/ {{if (seqlen){{print seqlen}}; print ;seqlen=0;next; }} {{ seqlen += length($0)}}END{{print seqlen}}' {fasta_file}", shell=True
)
reference_size: int = int(str(x).split('\\n')[1])
trf_results['reference_size'] = reference_size
ratios: float = sampling/reference_size
window = reference_size/sampling
trf_results['ratios'] = ratios

tr_bitvector = [0] * reference_size

with open(file_name, 'r', encoding='utf-8') as f:
    # Read the data
    for l in f:
        start, end = int(l.strip().split('\t')[1]), int(
            l.strip().split('\t')[2])
        for posx in range(start, end):
            tr_bitvector[posx] = 1

# Count number of bases in each window
for i in range(sampling):
    trf_results['tandem_repeats'][i] = sum(
        tr_bitvector[int(i*window):int((i+1)*window)])

# Save the results
with open(f'{file_name}.json', 'w', encoding='utf-8') as f:
    dump(trf_results, f)
