# Given a multi-fasta file, split it into individual fasta files
# Usage: python split_multifasta.py multifasta
# Creates one multifasta per individual sample
# Individual samples are identified by a common prefix in the headers

from sys import argv

multifasta = argv[1]
out = None

with open(multifasta) as f:
    for line in f:
        if line.startswith('>'):
            if out:
                out.close()
            sample = f"{line.split('#')[0][1:]}.{line.split('#')[1]}"
            out = open(f'{sample}.fasta', 'a')
            out.write(line)
        else:
            out.write(line)
    out.close()
