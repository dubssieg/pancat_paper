# Given an edition file, computes metrics on the size of editions

from sys import argv
from statistics import mean, median, stdev

edit_file: str = argv[1]
nodes_sizes_A: str = argv[2]
nodes_sizes_B: str = argv[3]

edition_sizes: list[int] = []
node_sizes_graph_A: dict[str, int] = {}
node_sizes_graph_B: dict[str, int] = {}

with open(nodes_sizes_A, 'r') as f:
    for line in f:
        node, size = line.strip().split('\t')
        node_sizes_graph_A[node] = int(size)

with open(nodes_sizes_B, 'r') as f:
    for line in f:
        node, size = line.strip().split('\t')
        node_sizes_graph_B[node] = int(size)

previous_breakpoint: int = float('-inf')
current_line: list[str] = None
next_breakpoint: int = float('inf')
current_path: str = ''
current_position: int = 0

with open(edit_file, 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        #
        if current_line:
            current_position = int(current_line[1])
            current_bpA = int(current_line[5])
            current_bpB = int(current_line[6])
            current_node_A = current_line[3]
            current_node_B = current_line[4]
            # We compute edition lengths (min between breakpoints)
            if current_position == current_bpA:
                edition_sizes.append(
                    min(
                        [abs(current_position - current_bpB), abs(current_position - (current_bpB-node_sizes_graph_B[current_node_B])), abs(current_position - previous_breakpoint), abs(current_position - next_breakpoint)]))
            else:
                edition_sizes.append(
                    min(
                        [abs(current_position - current_bpA), abs(current_position - (current_bpA-node_sizes_graph_A[current_node_A])), abs(current_position - previous_breakpoint), abs(current_position - next_breakpoint)]))

        current_line = line.strip().split('\t')
        if current_line[0] != current_path:
            current_path = current_line[0]
            previous_breakpoint: int = float('-inf')
            next_breakpoint: int = float('inf')


# Print mean, average, median, min, max, std deviation of edition sizes
print(f'Mean: {mean(edition_sizes)}')
print(f'Median: {median(edition_sizes)}')
print(f'Upper quartile: {median(edition_sizes[len(edition_sizes)//2:])}')
print(f'Lower quartile: {median(edition_sizes[:len(edition_sizes)//2])}')
print(f'Standard deviation: {stdev(edition_sizes)}')
print(f'Min: {min(edition_sizes)}')
print(f'Max: {max(edition_sizes)}')
