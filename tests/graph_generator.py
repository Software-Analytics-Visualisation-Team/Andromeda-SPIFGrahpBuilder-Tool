from rdflib import Graph
import node_construction
import edge_construction


def create_test_graph(create_nodes = False, create_edges = False):
    graph = Graph().parse("tests/test.owl", format='xml')
    graph.bind("ns1", "http://definitions.moonshot.sep/_#")
    graph.bind("SEON_general", "http://www.w3.org/2002/07/owl")
    graph.bind("SEON_main", "http://se-on.org/ontologies/general/2012/2/main.owl#")
    graph.bind("SEON_code", "http://se-on.org/ontologies/domain-specific/2012/02/code.owl#")

    if create_nodes:
        node_construction.create_primitive_nodes(graph)
        node_construction.create_container_nodes(graph)
        node_construction.create_structure_nodes(graph)

    if create_edges:
        edge_construction.create_container_contains_container_edges(graph)
        edge_construction.create_container_contains_structure_edges(graph)
        edge_construction.create_structure_contains_structure_edges(graph)
        edge_construction.create_extends_edges(graph)
        edge_construction.create_implements_edges(graph)
        edge_construction.create_accesses_edges(graph)
        edge_construction.create_calls_edges(graph)
        edge_construction.create_constructs_edges(graph)
        edge_construction.create_holds_edges(graph)
        edge_construction.create_accepts_edges(graph)
        edge_construction.create_returns_edges(graph)

    return graph
