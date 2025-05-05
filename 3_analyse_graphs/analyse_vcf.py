#!/usr/bin/env python3
from sys import argv
from json import dump
from subprocess import check_output
from typing import Any

# files should be a .vcf file issued from vg deconstruct
vcf_1: str = argv[1]
vcf_2: str = argv[2]
fasta_file: str = argv[3]
# change the sampling to change the number of windows over the genome
sampling: int = 200

vcf_results: dict[str, Any] = {
    'reference_size': 0,
    'shared_variants': [0] * sampling,
    'private_variants_A': [0] * sampling,
    'private_variants_B': [0] * sampling,
    'ratios': 0
}

file_A_variants: dict[str, tuple] = dict()
with open(vcf_1, 'r') as vcf_A:
    for line in vcf_A:
        if not line.startswith('#'):
            l: list[str] = line.split()
            file_A_variants[l[1]] = (l[3], l[4])

file_B_variants: dict[str, tuple] = dict()
with open(vcf_2, 'r') as vcf_B:
    for line in vcf_B:
        if not line.startswith('#'):
            l: list[str] = line.split()
            file_B_variants[l[1]] = (l[3], l[4])

x: str = check_output(
    f"awk '/^>/ {{if (seqlen){{print seqlen}}; print ;seqlen=0;next; }} {{ seqlen += length($0)}}END{{print seqlen}}' {fasta_file}", shell=True
)
reference_size: int = int(str(x).split('\\n')[1])
vcf_results['reference_size'] = reference_size
ratios: float = sampling/reference_size
vcf_results['ratios'] = ratios

for pos in file_A_variants.keys():
    if file_B_variants.get(pos, None) == file_A_variants.get(pos, None):
        vcf_results['shared_variants'][int(int(pos)*ratios)] += 1
    else:
        vcf_results['private_variants_A'][int(int(pos)*ratios)] += 1

for pos in file_B_variants.keys():
    if file_B_variants.get(pos, None) == file_A_variants.get(pos, None):
        vcf_results['shared_variants'][int(int(pos)*ratios)] += 1
    else:
        vcf_results['private_variants_B'][int(int(pos)*ratios)] += 1

# Save the results
with open(f'vcf_results.json', 'w', encoding='utf-8') as f:
    dump(vcf_results, f)
