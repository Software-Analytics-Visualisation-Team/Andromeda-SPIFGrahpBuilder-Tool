from json_construction import construct_json_from_nodes_and_edges
from rdflib import Graph
from node_construction import (
    create_primitive_nodes,
    create_container_nodes,
    create_structure_nodes,
)
from edge_construction import (
    create_accesses_edges,
    create_container_contains_container_edges,
    create_container_contains_structure_edges,
    create_structure_contains_structure_edges,
    create_extends_edges,
    create_implements_edges,
    create_calls_edges,
    create_constructs_edges,
    create_holds_edges,
    create_accepts_edges,
    create_returns_edges,
)
import sys

if __name__ == "__main__":

    # Get the input and output file paths from the command line arguments.
    input_file_path, output_file_path = sys.argv[1], sys.argv[2]

    # Parse the input file as a graph.
    g = Graph().parse(input_file_path, format='xml')
    g.bind("ns1", "http://definitions.moonshot.sep/_#")
    g.bind("SEON_general", "http://www.w3.org/2002/07/owl")
    g.bind("SEON_main", "http://se-on.org/ontologies/general/2012/2/main.owl#")
    g.bind("SEON_code", "http://se-on.org/ontologies/domain-specific/2012/02/code.owl#")

    # Create nodes
    create_primitive_nodes(g)
    create_container_nodes(g)
    create_structure_nodes(g)

    # Create edges
    create_container_contains_container_edges(g)
    create_container_contains_structure_edges(g)
    create_structure_contains_structure_edges(g)
    create_extends_edges(g)
    create_implements_edges(g)
    create_accesses_edges(g)
    create_calls_edges(g)
    create_constructs_edges(g)
    create_holds_edges(g)
    create_accepts_edges(g)
    create_returns_edges(g)

    # Output the constructed json to a file.
    with open(output_file_path, "w") as f:
        f.write(construct_json_from_nodes_and_edges())
