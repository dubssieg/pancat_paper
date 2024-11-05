#!/bin/bash
#SBATCH --job-name=ymgc
#SBATCH --cpus-per-task=16
#SBATCH --mem=128G
#SBATCH --constraint avx2


###################################################################
#
# This script builds a pangenome graph from assemblies in separated files
# + assemblies must be in .fasta/.fa format
# + one file per specimen, can contain multiple headers
#
###################################################################


# Defining envs
ENVS="./"
ENV_CACTUS="cactus_2.9.0"
VENV_CACTUS="software/cactus-bin-v2.9.0/venv-cactus-v2.9.0/bin/activate"

# Working dirs
PROJECT="./"

OUTPUT=$PROJECT"OUT_MGC/"
PIPELINE=$PROJECT"PIPELINE_MGC/"
DATAS=$PROJECT"YEAST_DATA/"
TOIL=$PROJECT"JS/"
TEMP=$PROJECT"TEMP/"

# Loading env
. /local/env/envconda.sh
conda activate $ENV_CACTUS
source $VENV_CACTUS

# Creating dirs
mkdir -p $OUTPUT $PIPELINE $TOIL $TEMP

python cactus_file.py

# Creating graphs
VAR=$((1))
for FILE in $PIPELINE*
do
    # Getting reference name (first line in file before \t)
    echo "$(head -n 1 $FILE)" | cut -d$'\t' -f1 > $TEMP"tempfile.txt"
    NAME_REF=`cat $TEMP"tempfile.txt"`
    JB=$TOIL".js_"$VAR
    [ -d $JB ] && rm -r $JB
    mkdir $OUTPUT"CACTUS_"$VAR
    OUT=$OUTPUT"CACTUS_"$VAR"/graph"
    mkdir $OUTPUT"CACTUS_"$VAR"/workdir"
    mkdir $OUTPUT"CACTUS_"$VAR"/outdir"
    cactus-minigraph $JB $FILE $OUT.gfa --reference $NAME_REF --binariesMode singularity #--configFile cactus_config.xml
    cactus-graphmap $JB $FILE $OUT.gfa $OUT.paf  --reference $NAME_REF --outputFasta $OUT.sv.gfa.fa.gz --binariesMode singularity #--configFile cactus_config.xml
    cactus-align $JB $FILE $OUT.paf $OUT.hal --pangenome --outGFA --outVG --reference $NAME_REF --workDir $OUTPUT"CACTUS_"$VAR"/workdir" --binariesMode singularity #--configFile cactus_config.xml
    cactus-graphmap-join $JB --vg $OUT.vg --outDir $OUTPUT"CACTUS_"$VAR"/outdir" --outName "final" --reference $NAME_REF --clip 0 --filter 0 --binariesMode singularity #--configFile cactus_config.xml
    if [ -d $JB ]
    then
        rm -r $JB
    fi
    GRAPH=$OUTPUT"CACTUS_"$VAR"/outdir/final.full.gfa"
    gzip -d $GRAPH".gz"
    mv $GRAPH $OFFSET"graph_"$VAR".gfa"
    #sed -i "1d; $d;" $FILE
    VAR=$((VAR+1))
done

conda deactivate
