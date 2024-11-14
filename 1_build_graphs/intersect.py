# Writes to standard output intersection between two path files
# Usage: python intersect.py path1 path2

from sys import argv

path1, path2 = argv[1], argv[2]

with open(path1) as f:
    path1 = [
        x.split('\t')[0] for x in f.read().splitlines() if not x.startswith('#')
    ]

with open(path2) as f:
    path2 = [
        x.split('\t')[0] for x in f.read().splitlines() if not x.startswith('#')
    ]

intersection = set(path1) & set(path2)

for i in intersection:
    print(i)
