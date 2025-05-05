# Given an edition file, computes metrics on the size of editions

from sys import argv
from statistics import mean, median, stdev

edit_file: str = argv[1]

# We consider only edits on small nodes
node_length_threshold: int = 50
edits_on_large_nodes: int = 0

current_path: str = ''
current_pos: int = 0
current_bpA: int = 0
current_bpB: int = 0

edition_sizes: list[int] = []
node_sizes_graph_A: dict[str, int] = []
node_sizes_graph_B: dict[str, int] = []


with open(edit_file, 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        else:
            path, pos, _, _, _, bpA, bpB = line.strip().split('\t')
        if path != current_path:
            current_path = path
            current_pos = 0
            current_bpA = 0
            current_bpB = 0

        # We get current node lengths
        if current_bpA != int(bpA):
            nodeA_size = abs(int(bpA) - current_bpA)
        if current_bpB != int(bpB):
            nodeB_size = abs(int(bpB) - current_bpB)

        # We compute edition lengths (min between breakpoints)
        if int(pos) == int(bpA):
            current_bpA = int(bpA)
            if nodeB_size <= node_length_threshold:
                edition_sizes.append(
                    min(abs(int(pos) - current_bpB), abs(int(pos) - int(bpB)))
                )
            else:
                edits_on_large_nodes += 1
        elif int(pos) == int(bpB):
            current_bpB = int(bpB)
            if nodeA_size <= node_length_threshold:
                edition_sizes.append(
                    min(abs(int(pos) - current_bpA), abs(int(pos) - int(bpA)))
                )
            else:
                edits_on_large_nodes += 1
        else:
            print('Error: breakpoint not found in position')
        current_pos = int(pos)


# Print mean, average, median, min, max, std deviation of edition sizes
print(f'Mean: {mean(edition_sizes)}')
print(f'Median: {median(edition_sizes)}')
print(f'Upper quartile: {median(edition_sizes[len(edition_sizes)//2:])}')
print(f'Lower quartile: {median(edition_sizes[:len(edition_sizes)//2])}')
print(f'Standard deviation: {stdev(edition_sizes)}')
print(f'Min: {min(edition_sizes)}')
print(f'Max: {max(edition_sizes)}')
print(
    f'Edits on large nodes: {(edits_on_large_nodes/(edits_on_large_nodes+len(edition_sizes)))*100}%')
