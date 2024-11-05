The file `pipeline_file.txt` is an example of pipeline files used by the scripts. You put the name for your haplotype in the first column, then the (preferably) absolute path to the `.fasta`/`.fa` file.

The script `build_mgc.sh` constructs the graphs for every pipeline file in the pipeline folder with minigraph-cactus. Please note that minigraph-cactus does edit these files, so keep a safe copy of them to use with `build_pggb.sh`.

Data to run the scripts is available on [Zenodo](https://doi.org/10.5281/zenodo.10932490).