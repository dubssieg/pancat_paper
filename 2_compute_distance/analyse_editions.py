#!/usr/bin/env python3
from sys import argv
from json import dump
from typing import Any

# file should be a .tsv file issued from rs-pancat-compare
file_name: str = argv[1]
# change the sampling to change the number of windows over the genome
sampling: int = 200
edition_results: dict = {}
merges_results: dict = {}
splits_results: dict = {}
ratios_paths: dict = {}
path_lengths: dict = {}

edits_results: dict[str, Any] = {
    'editions': {},
    'ratios': {},
    'lengths': {},
    'merges': {},
    'splits': {}
}

with open(file_name, 'r', encoding='utf-8') as f:
    # Skip the header
    next(f)
    # Read the path sizes
    while (l := next(f)).startswith('##'):
        path_name, path_length = l[3:].strip().split('\t')
        path_lengths[path_name] = int(path_length)
        ratios_paths[path_name] = sampling/int(path_length)
    # Skip the header
    next(f)
    # Init the results
    for path_name in ratios_paths.keys():
        edition_results[path_name] = [0] * sampling
        merges_results[path_name] = [0] * sampling
        splits_results[path_name] = [0] * sampling
    # Read the data
    for l in f:
        if l.startswith('#'):
            continue
        else:
            path_name, position, operation, nodeA, nodeB, breakpointA, breakpointB = l.strip().split(
                '\t')
            if operation == 'S':
                splits_results[path_name][int(
                    int(position)*ratios_paths[path_name])] += 1
            elif operation == 'M':
                merges_results[path_name][int(
                    int(position)*ratios_paths[path_name])] += 1
            edition_results[path_name][int(
                int(position)*ratios_paths[path_name])] += 1

edits_results['editions'] = edition_results
edits_results['ratios'] = ratios_paths
edits_results['lengths'] = path_lengths
edits_results['merges'] = merges_results
edits_results['splits'] = splits_results

# Save the results
with open(f'{file_name}.json', 'w', encoding='utf-8') as f:
    dump(edits_results, f)
