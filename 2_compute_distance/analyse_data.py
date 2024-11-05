#!/usr/bin/env python3
from sys import argv
from json import dump

# file should be a .tsv file issued from rs-pancat-compare
file_name: str = argv[1]
# change the sampling to change the number of windows over the genome
sampling: int = 200
edition_results: dict = {}
path_sizes: dict = {}

with open(file_name, 'r', encoding='utf-8') as f:
    # Skip the header
    next(f)
    # Read the path sizes
    while (l := next(f)).startswith('##'):
        path_name, path_length = l[3:].strip().split('\t')
        path_sizes[path_name] = int(path_length)
    # Skip the header
    next(f)
    # Init the results
    for path_name, path_length in path_sizes.items():
        edition_results[path_name] = [0] * sampling
    # Read the data
    for l in f:
        if l.startswith('#'):
            continue
        else:
            path_name, position, operation, nodeA, nodeB, breakpointA, breakpointB = l.strip().split(
                '\t')
            # You can filter operations here to get merges and splits
            # if operation == 'S':
            # do something relevant
            # else:
            # do something relevant
            ratios: float = sampling/path_sizes[path_name]
            edition_results[path_name][int(int(position)*ratios)] += 1

# Save the results
with open(f'{file_name}.json', 'w', encoding='utf-8') as f:
    dump(edition_results, f)
