The distance can be computed using [rs-pancat-compare](https://github.com/dubssieg/rs-pancat-compare).
Commands can be found in `distance.sh`.

All graphs should be with paths in a GFA1.0 format. For Minigraph-Cactus file, it is possible to use the `vg` toolkit with the command `vg convert in.gfa -W -f > out.gfa` to convert W-lines to P-lines, ensuring we have a GFA1.0.

As the comparison is made upon path names, it is recommanded to check (for instance with `rs-pancat-paths graph.gfa > path_names.tsv`) the names of the path to see if they match between the two files that we want to compare.

It outputs a `.tsv` file that you should use as input of `analyse_data.py`.
This script tidy the data for the next step (analysis with notebooks)
You can change the number of sectors (windows over the length of the graph) by modifying the script.