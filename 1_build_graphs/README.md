# Yeast graphs

The file `pipeline_file.txt` is an example of pipeline files used by the scripts. You put the name for your haplotype in the first column, then the (preferably) absolute path to the `.fasta`/`.fa` file.

The script `build_mgc.sh` constructs the graphs for every pipeline file in the pipeline folder with minigraph-cactus. Please note that minigraph-cactus does edit these files, so keep a safe copy of them to use with `build_pggb.sh`.

Data to run the scripts is available on [Zenodo](https://doi.org/10.5281/zenodo.10932490).

# Consensus human graphs

First, we extract pathlists in both graphs (mgc and pggb) from the HPRC resources. We use rs-pangenome-paths (avaliable as a submodule).

```bash
rs-pancat-paths pggb_human_21.gfa > human_21_pggb.tsv
rs-pancat-paths mgc_human_21.gfa > mgc_21_pggb.tsv
```

Then we compute the intersection file of paths.

```bash
python intersect.py human_21_mgc.tsv human_21_pggb.tsv > human_21.txt
```

After, we extract the corresponding sequences from the graph using rs-pangenome-reconstruct (avaliable as a submodule). As we only need to do it on one of the two graphs, we select the light one (the mgc one).

```bash
rs-pancat-reconstruct mgc_human_21.gfa human_21.txt > human_21_intersect.fa
```

At this point we have a big `multifasta` file containing all the common sequences. It is ready for pggb, but not for minigraph-cactus (needs one `multifasta` per sample, and a pipeline table to know where to take the sequences as input).

```bash
python split_multifasta.py human_21_intersect.fa
```

Finally, we can apply the same steps as for the yeast graphs construction.