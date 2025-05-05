#!/usr/bin/env python3
from sys import argv
from json import dump
from subprocess import check_output
from typing import Any
from gfagraphs import Graph


# file should be a .bed file issued from the conversion of the .dat TRF file
file_name: str = "nodes_results.json"
gfa_file_A: str = argv[1]
gfa_file_B: str = argv[2]
reference: str = argv[3]
fasta_file: str = argv[4]
# change the sampling to change the number of windows over the genome
sampling: int = 200

nodes_results: dict[str, Any] = {
    'reference_size': 0,
    'nodes_A': [0] * sampling,
    'nodes_B': [0] * sampling,
}

ld: str = check_output(
    f"awk '/^>/ {{if (seqlen){{print seqlen}}; print ;seqlen=0;next; }} {{ seqlen += length($0)}}END{{print seqlen}}' {fasta_file}", shell=True
)
reference_size: int = int(str(ld).split('\\n')[1])

ratios: float = sampling/reference_size

graph_A = Graph(gfa_file_A)
pos_counter: int = 0
for x, _ in graph_A.paths[reference.upper()]['path']:
    nodes_results['nodes_A'][int(float(pos_counter)*ratios)] += 1
    pos_counter += graph_A.segments[x]['length']

graph_B = Graph(gfa_file_B)
pos_counter: int = 0
for x, _ in graph_B.paths[reference.upper()]['path']:
    nodes_results['nodes_B'][int(float(pos_counter)*ratios)] += 1
    pos_counter += graph_B.segments[x]['length']

nodes_results['reference_size'] = reference_size
ratios: float = sampling/reference_size
nodes_results['ratios'] = ratios


# Save the results
with open(f'{file_name}.json', 'w', encoding='utf-8') as f:
    dump(nodes_results, f)
