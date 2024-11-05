# Notebooks on pangenome graph edition

> [!NOTE]\
> The present repository contains Jupyter Notebooks and scripts that aims to analyse how two graphs, build with the same set of genomes, can differ. Data used in this experiment is available on [Zenodo](https://doi.org/10.5281/zenodo.10932490).

Graph edition is a vastly studied subject, with many heuristics to compare topologies, and many NP-hard problems. Here, we present a method, relying on the specificities of what a pangenome graph is (a collection of subsequences linked by edges, that represents the embedding of genomes inside a graph structure) to formulate a O(n) solution in this specific case. It allows us to pinpoint dissimilarities between graphs, and we can analyse how such graphs differ when build with different tools, or parameters.

# Creating/getting the graphs

We applied our distance to graphs built from two collections of genomes: telomere-to-telomere yeast assemblies[[1](https://www.nature.com/articles/s41588-023-01459-y)] and the HPRC human draft pangenome [[2](https://www.nature.com/articles/s41586-023-05896-x)].

## Yeast dataset

From the yeast assemblies, we gathered the sequences for each chromosome. We selected chromosome 1 from 15 samples and constructed the graphs using the [Minigraph-Cactus pipeline](https://github.com/ComparativeGenomicsToolkit/cactus) (*mgc*, v2.9.0) and the [PanGenome Graph Builder](https://github.com/pangenome/pggb) (*pggb*, v0.6.0).
Graphs built with *mgc* had the clip and filter parameters set to zero, ensuring that the entire sequence was embedded in the structure. Both tools were run with all other parameters kept at their default settings. The graphs did not undergo any post-processing, and graphs from *pggb* were collected before the smoothxg step to ensure completeness.

Scripts used to build the graphs are available [here](https://github.com/dubssieg/pancat_paper/1_build_graphs).

## Human dataset

Human graphs were used without post-processing and are avaiable [here for the mgc version](https://s3-us-west-2.amazonaws.com/human-pangenomics/index.html?prefix=pangenomes/freeze/freeze1/minigraph-cactus/hprc-v1.1-mc-chm13/hprc-v1.1-mc-chm13.chroms), and [here for the pggb version](https://s3-us-west-2.amazonaws.com/human-pangenomics/index.html?prefix=pangenomes/freeze/freeze1/pggb/chroms/).

Used graphs from mgc are the `.full.og` ones, converted to GFA1.0 using [odgi](https://github.com/pangenome/odgi) (v0.9.0-0-g1895f496).

```bash
odgi view -g -i $INPUT > $OUTPUT
```

Names of the two haplotypes GRCH38 and CHM13 were standardized across the two files with `sed` before comparing the graphs.

```bash
sed -i 's/grch38/GRCH38/g;s/chm13/CHM13/g' graph.gfa
```

# Edition computation between graphs

All editions between graphs are computed using [rs-pancat-compare](https://github.com/dubssieg/rs-pancat-compare) (v0.1.0). Yeast graphs and supplementary data are available on [Zenodo](https://doi.org/10.5281/zenodo.10932490). When comparing graphs between mgc and pggb, editions are always computed in the order to get the pggb graph out of the mgc graph. As output, we get a tab-separated file containing path name, a position in the haplotype, a one-letter encoding of the operation, and nodes that the operation applies to in first and second graph. 

Data is pre-processed using scripts available [here](https://github.com/dubssieg/pancat_paper/2_compute_distance).

# Sequence and graph analysis

All commands are available [in the dedicated folder](https://github.com/dubssieg/pancat_paper/3_analyse_graphs).

All variants were computed using vg deconstruct (v1.56.0). Tandem repeats were computed using TandemRepeat Finder (v4.09.1) and selected using bedtools intersect (v2.31.1).
From the yeast assemblies, we built multiple graphs, varying the number of included samples (from 2 to 15), the reference sample for *mgc*, the order of secondary genomes, and tool versions. For each graph built with *mgc*, we also constructed a corresponding *pggb* graph with identical properties (where applicable), ensuring that all comparisons were made between graphs representing the same input data exactly. Once built, we verified that the graphs were complete pangenome graphs.

We also analyzed differences between *mgc* and *pggb* graphs from the HPRC dataset (year 1) for chromosomes 1 and 21 individually. We computed edits between the full mgc CHM13 graph (mgc v2.6.4), without clipping or filtering, and the *pggb* graph (pggb v0.2.0+531f85f). Variants are extracted from the raw CHM13 VCFs supplied along the pangenomes.

# Reproduce the figures from the article

Edition file is subsequently processed using Jupyter Notebooks [available in this repository](https://github.com/dubssieg/pancat_paper/4_reproduce_figures). Timings and memory consumption were recorded using heaptrack.