# Variant calling

This step requires to have `vg toolkit` installed. We used version 1.56.0 of `vg`. You can find [the software here](https://github.com/vgteam/vg).

We used the command `vg paths -Mx $GRAPH` to het the name of the haplotypes in the graph and choose the reference accordingly.
For the graph issued from `minigraph-cactus`, we used the command `vg convert $INPUT_GRAPH -W -f > $OUTPUT_GRAPH` to convert it from `GFA1.1` to `GFA1.0`.

Then, we computed variant bubbles using `vg deconstruct -e -a -p $REF_NAME $GRAPH > $VCF_OUTPUT`. The file was later on used as input of the notebooks [you can find here](https://github.com/dubssieg/pancat_paper/4_reproduce_figures).

# Tandem repeats and *k*-mer analysis

Tandem repeats were computed using [Tandem Repeat Finder](https://github.com/Benson-Genomics-Lab/TRF) (TRF) using command `trf $FASTA 2 7 7 80 10 50 500 -f -d -m`. Then, TR were converted from `.dat` to `.bed` using the script [available here](https://github.com/hdashnow/TandemRepeatFinder_scripts/blob/master/TRFdat_to_bed.py). Subsequently, we made the intersection between TR and variants from each of the graphs, using `bedtools intersect` (v2.31.1) with the command `bedtools intersect -a $VARIANTS_VCF -b $TRF_BED > $INTERSECT_BED`

*k*-mer analysis was made using this python code:

```python
kmers:list = [set() for _ in range(sampling)]
ratios:float = sampling/seq_len
for i in range(seq_len-ksize):
    kmers[int(int(i)*ratios)].add(sequence[i:i+ksize])
```