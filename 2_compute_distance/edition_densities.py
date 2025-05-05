from sys import argv

# file should be a .tsv file issued from rs-pancat-compare
file_name: str = argv[1]

# We will check the top edited nodes (nodes with the most editions)
top_nodes_A: dict[str, int] = {}
top_nodes_B: dict[str, int] = {}

with open(file_name, 'r', encoding='utf-8') as f:
    for l in f:
        if not l.startswith('#'):
            path, position, operation, nodeA, nodeB, breakpointA, breakpointB = l.strip().split('\t')
            if nodeA in top_nodes_A:
                top_nodes_A[nodeA] += 1
            else:
                top_nodes_A[nodeA] = 1
            if nodeB in top_nodes_B:
                top_nodes_B[nodeB] += 1
            else:
                top_nodes_B[nodeB] = 1

# Sort the nodes by number of editions
top_nodes_A = dict(
    sorted(top_nodes_A.items(), key=lambda item: item[1], reverse=True))
top_nodes_B = dict(
    sorted(top_nodes_B.items(), key=lambda item: item[1], reverse=True))

# Print the top 10 nodes
print('Top 10 nodes in graph A:')
for node, count in list(top_nodes_A.items())[:10]:
    print(f'{node}: {count} editions')
print('Top 10 nodes in graph B:')
for node, count in list(top_nodes_B.items())[:10]:
    print(f'{node}: {count} editions')
