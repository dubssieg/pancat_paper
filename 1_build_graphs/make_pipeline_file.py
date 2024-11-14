# Creates a pipeline file given a folder containing multifasta files
# Usage: python make_pipeline_file.py folder
# For each multifasta file in the folder, creates a line in the pipeline file (written to stdout)
# Line features the name of the sample (base name of the multifasta file) and the absolute path to the multifasta file

from sys import argv
from os import listdir, path

folder = argv[1]
files = listdir(folder)

for file in files:
    print(f"{file.split('.')[0]}\t{path.abspath(path.join(folder, file))}")
