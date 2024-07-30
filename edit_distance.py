from argparse import ArgumentParser
from tharospytools.multithreading import futures_collector
from re import split
from rich.traceback import install
from pathlib import Path
from os.path import join
install(show_locals=True)


def perform_edition(
        gfa_A: str,
        gfa_B: str,
) -> tuple:
    """
    In this function, we do calculate the distance between G1 and G2, by trying to modify G2 into G1.
    Note the two graphs can be freely swapped, we just need to invert scores for reciprocal events and operations

    Args:
        gfa_A (str): a path to a gfa file
        gfa_B (str): a path to another gfa file
    """
    # We build a folder for results
    Path(output_folder := f"pancat_{Path(gfa_A).stem}_vs_{Path(gfa_B).stem}").mkdir(
        parents=True, exist_ok=True)

    segs_A: dict[str, int] = dict()
    paths_A: dict[str, list[str]] = dict()
    with open(gfa_A, 'r', encoding='utf-8') as gfareader:
        for line in gfareader:
            if line.startswith('S'):
                segs_A[line.split('\t')[1]] = len(line.split('\t')[2].strip())
            elif line.startswith('P'):
                paths_A[line.split('\t')[1]] = [x[:-1]
                                                for x in line.split('\t')[2].strip().split(',')]
            elif line.startswith('W'):
                paths_A[line.split('\t')[1]] = [x for x in split(
                    '<|>', line.split('\t')[6].strip()[1:])]

    segs_B: dict[str, int] = dict()
    paths_B: dict[str, list[str]] = dict()
    with open(gfa_B, 'r', encoding='utf-8') as gfareader:
        for line in gfareader:
            if line.startswith('S'):
                segs_B[line.split('\t')[1]] = len(line.split('\t')[2].strip())
            elif line.startswith('P'):
                paths_B[line.split('\t')[1]] = [x[:-1]
                                                for x in line.split('\t')[2].strip().split(',')]
            elif line.startswith('W'):
                paths_B[line.split('\t')[1]] = [x for x in split(
                    '<|>', line.split('\t')[6].strip()[1:])]

    # We compute the intersection of paths in both graphs
    path_intersect: set[str] = set(
        paths_A.keys()
    ).intersection(
        set(paths_B.keys())
    )

    ___: list = path_level_edition(
        segs_A,
        paths_A,
        segs_B,
        paths_B,
        path_intersect,
        output_folder,
    )


def path_level_edition(
    segments_A: dict,
    pathlists_A: dict,
    segments_B: dict,
    pathlists_B: dict,
    selected_paths: set[str],
    output_folder: str,
) -> list:
    """Compute edition, path by path, between the two graphs.
    The graph_A will be used as reference

    Args:
        selected_paths (set[str]): the paths where the edition needs to be computed

    Returns:
        dict: results of edition
    """
    return futures_collector(
        func=edit_single_path_path_level,
        argslist=[
            (
                path_name,
                segments_A,
                pathlists_A[path_name],
                segments_B,
                pathlists_B[path_name],
                output_folder,
            ) for path_name in selected_paths
        ]
    )


def edit_single_path_path_level(
    path_name: str,
    segs_A: dict[str, int],
    pathlist_A: list[str],
    segs_B: dict[str, int],
    pathlist_B: list[str],
    output_folder: str,
) -> None:
    """Performs the edition over a single path

    Args:
        path_name (str): name of the path
        graph_A (Graph): first graph
        graph_B (Graph): second graph

    Raises:
        ValueError: if no edition is forseeable

    Returns:
        dict: editions
    """
    with open(join(output_folder, f'{path_name}.log'), 'w', encoding='utf-8') as editfile:
        print("#PATH\tTYPE\tPOS\tSEG_A\tSEG_B", file=editfile)

        i: int = 0  # counter of segmentations on graph_A
        j: int = 0  # counter of segmentations on graph_B

        pos_A: int = 0  # Absolute position in BP on A
        pos_B: int = 0  # Absolute position in BP on B

        global_pos: int = 0  # Position across both genomes

        # Iterating until we did not go through both segmentations
        while i < len(pathlist_A) and j < len(pathlist_B):
            # Currently evaluated nodes
            current_node_A: str = pathlist_A[i]
            current_node_B: str = pathlist_B[j]

            # We compute the next closest breakpoint
            global_pos = min(
                global_pos +
                (
                    segs_A[current_node_A]-(global_pos-pos_A)
                ),
                global_pos +
                (
                    segs_B[current_node_B]-(global_pos-pos_B)
                )
            )

            # We added the interval to current positions
            match (global_pos-pos_A == segs_A[current_node_A], global_pos-pos_B == segs_B[current_node_B]):
                case (True, True):
                    # Iterating on both, no edition needed
                    pos_A += segs_A[current_node_A]
                    pos_B += segs_B[current_node_B]
                    i += 1
                    j += 1
                case (True, False):
                    # Iterating on top, split required
                    print(
                        f"{path_name}\tS\t{global_pos}\t{current_node_A}\t{current_node_B}", file=editfile
                    )
                    pos_A += segs_A[current_node_A]
                    i += 1
                case (False, True):
                    # Iterating on bottom, merge required
                    print(
                        f"{path_name}\tM\t{global_pos}\t{current_node_A}\t{current_node_B}", file=editfile
                    )
                    pos_A += segs_B[current_node_B]
                    j += 1
                case (False, False):
                    raise ValueError()


######################## PARSER ########################


parser: ArgumentParser = ArgumentParser()

parser.add_argument(
    "graph_A",
    type=str,
)

parser.add_argument(
    "graph_B",
    type=str,
)

args = parser.parse_args()

if __name__ == "__main__":
    perform_edition(args.graph_A, args.graph_B)
