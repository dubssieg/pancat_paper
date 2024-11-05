git clone https://github.com/dubssieg/rs-pancat-compare.git
cd rs-pancat-compare
cargo build

GRAPH1="graph_A.gfa"
GRAPH2="graph_B.gfa"
OUTPUT_FILE="distance.tsv"

./target/debug/rs-pancat-compare $GRAPH1 $GRAPH2 > $OUTPUT_FILE