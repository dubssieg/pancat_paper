#!/bin/bash
#SBATCH --job-name=ypggb
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G

###################################################################
#
# This script builds a pangenome graph from assemblies in separated files
# + assemblies must be in .fasta/.fa format
# + one file per specimen, can contain multiple headers
#
###################################################################

# Defining envs
ENVS="./"
ENV_PGGB=pggb_0.6.0 #$ENVS"pggb"

# Working dirs
PROJECT="./"


OUTPUT=$PROJECT"OUT_PGGB/"
PIPELINE=$PROJECT"PIPELINE_PGGB/"
PGGB=$PROJECT"genomes_merge/"
DATAS=$PROJECT"YEAST_DATA/"


# Loading env
. /local/env/envconda.sh
conda activate $ENV_PGGB

# Creating dirs
mkdir -p $OUTPUT $PIPELINE $PGGB


VAR=$((1))
for FILE in $PIPELINE*
do
    cat $(awk '{print $2}' $FILE) > $PGGB"yeast_"$VAR".fa"
    samtools faidx $PGGB"yeast_"$VAR".fa"
    
    #Getting number of haplotypes in the future graph
    COUNT="$(sed -n '$=' $FILE)"
    
    # Creating the variation graph
    pggb -i $PGGB"yeast_"$VAR".fa" -o $OUTPUT -n $COUNT -t 8 -p 90 -s 5k # -V $NAME_REF":#:1"
    VAR=$((VAR+1))
done

conda deactivate