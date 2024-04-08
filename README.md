# Notebooks on pangenome graph edition

> [!NOTE]\
> The present repository contains jupyter notebooks that aims to analyse how two graphs, build with the same set of genomes, can differ. Data used in this experiment is available on [Zenodo](https://doi.org/10.5281/zenodo.10932490).

Graph edition is a vastly studied subject, with many heuristics to compare topologies, and many NP-hard problems. Here, we present a method, relying on the specificities of what a pangenome graph is (a collection of subsequences linked by edges, that represents the embedding of genomes inside a graph structure) to formulate a O(n.m) solution in this specific case. It allows us to pinpoint dissimilarities between graphs, and we can analyse how such graphs differ when build with different tools, or parameters.