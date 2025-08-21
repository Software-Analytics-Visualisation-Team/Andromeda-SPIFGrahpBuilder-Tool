from rdflib import Graph
from json_construction import Edge, add_edge
from helpers import namespace_to_id
from node_construction import ID_ALIAS


def create_container_contains_container_edges(g: Graph):
    """ Create edges from a container to the containers it contains."""

    # Construct the query.
    create_container_contains_container_query = """
        SELECT ?resource ?hasIdentifier ?hasNestedNamespaceMember ?nestedIdentifier
        WHERE {
            VALUES ?type {
                <http://se-on.org/ontologies/system-specific/2012/02/java.owl#JavaPackage>
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#Namespace>
            }
            ?resource rdf:type ?type . 
            ?resource SEON_code:hasIdentifier ?hasIdentifier .
            ?resource SEON_code:hasNestedNamespaceMember ?hasNestedNamespaceMember .
            ?hasNestedNamespaceMember SEON_code:hasIdentifier ?nestedIdentifier .
        }
    """
    create_container_contains_container_query_result = g.query(create_container_contains_container_query)
    # Construct the edges.
    for row in create_container_contains_container_query_result:
        # edge = Edge(
        #     namespace_to_id(row["resource"]),
        #     namespace_to_id(row["hasNestedNamespaceMember"]),
        #     1,
        #     "contains",
        # )
        source = ID_ALIAS.get(row["hasIdentifier"].toPython(),
                            row["hasIdentifier"].toPython())
        target = ID_ALIAS.get(row["nestedIdentifier"].toPython(),
                            row["nestedIdentifier"].toPython())
        edge = Edge(source, target, 1, "contains")

        add_edge(edge)


def create_container_contains_structure_edges(g: Graph):
    """ Create edges from a container to the structures it contains."""

    # Construct the query.
    create_container_contains_structure_query = """
        SELECT ?resource ?hasIdentifier ?isNamespaceMemberOf ?namespaceIdentifier
        WHERE {
            VALUES ?type {
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#ClassType>
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#EnumerationType>
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#InterfaceType>
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#Datatype>
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#ExceptionType>
            } 
            ?resource rdf:type ?type . ?resource SEON_code:hasIdentifier ?hasIdentifier .
            ?resource SEON_code:isNamespaceMemberOf ?isNamespaceMemberOf .
            ?isNamespaceMemberOf SEON_code:hasIdentifier ?namespaceIdentifier .
        }
    """
    create_container_contains_structure_query_result = g.query(create_container_contains_structure_query)
    # Construct the edges.
    for row in create_container_contains_structure_query_result:
        # edge = Edge(
        #     namespace_to_id(row["isNamespaceMemberOf"]),
        #     namespace_to_id(row["resource"]),
        #     1,
        #     "contains",
        # )
        source = row["namespaceIdentifier"].toPython()
        target = row["hasIdentifier"].toPython()
        # remap if duplicate id
        source = ID_ALIAS.get(source, source)
        target = ID_ALIAS.get(target, target)
        edge = Edge(source, target, 1, "contains")
        edge.add_property("containmentType", "package")
        add_edge(edge)


def create_structure_contains_structure_edges(g: Graph):
    """ Create edges from a structure to the structures it contains."""

    # Construct the query.
    create_structure_contains_structure_query = """
        SELECT ?resource ?hasIdentifier ?hasNestedComplexTypeMember ?nestedIdentifier
        WHERE { VALUES ?type { <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#InterfaceType>
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#ClassType>
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#EnumerationType>
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#AnnotationType>
            }
            ?resource rdf:type ?type . 
            ?resource SEON_code:hasIdentifier ?hasIdentifier .
            ?resource SEON_code:hasNestedComplexTypeMember ?hasNestedComplexTypeMember .
            ?hasNestedComplexTypeMember SEON_code:hasIdentifier ?nestedIdentifier .
        }
    """
    create_structure_contains_structure_query_result = g.query(create_structure_contains_structure_query)
    # Construct the edges.
    for row in create_structure_contains_structure_query_result:
        # edge = Edge(
        #     namespace_to_id(row["resource"]),
        #     namespace_to_id(row["hasNestedComplexTypeMember"]),
        #     1,
        #     "contains",
        # )
        source = ID_ALIAS.get(row["hasIdentifier"].toPython(), row["hasIdentifier"].toPython())
        target = ID_ALIAS.get(row["nestedIdentifier"].toPython(), row["nestedIdentifier"].toPython())
        edge = Edge(source, target, 1, "contains")

        edge.add_property("containmentType", "nested class")
        add_edge(edge)


def create_extends_edges(g: Graph):
    """ Create edges from a class to the classes it extends."""

    # Construct the query.
    # For classes extending classes.
    create_extends_query = """
        SELECT ?resource ?hasIdentifier ?hasSuperClass
        WHERE {
            VALUES ?type {
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#ClassType>
            }
            ?resource rdf:type ?type . 
            ?resource SEON_code:hasIdentifier ?hasIdentifier .
            ?resource SEON_code:hasSuperClass ?hasSuperClass .
        }
    """
    create_extends_query_result = g.query(create_extends_query)
    # Construct the edges.
    for row in create_extends_query_result:
        edge = Edge(
            namespace_to_id(row["resource"]),
            namespace_to_id(row["hasSuperClass"]),
            1,
            "specializes",
        )
        edge.add_property("specializationType", "extends")
        add_edge(edge)

    # Construct the query.
    # For interfaces extending interfaces.
    create_extends_query = """
        SELECT ?resource ?hasIdentifier ?hasSuperInterface
        WHERE { VALUES ?type {
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#InterfaceType>
            }
            ?resource rdf:type ?type .
            ?resource SEON_code:hasIdentifier ?hasIdentifier .
            ?resource SEON_code:hasSuperInterface ?hasSuperInterface .
        }
    """
    create_extends_query_result = g.query(create_extends_query)
    # Construct the edges.
    for row in create_extends_query_result:
        edge = Edge(
            namespace_to_id(row["resource"]),
            namespace_to_id(row["hasSuperInterface"]),
            1,
            "specializes",
        )
        edge.add_property("specializationType", "extends")
        add_edge(edge)
        

def create_implements_edges(g: Graph):
    """ Create edges from a class to the interfaces it implements."""

    # Construct the query.
    create_implements_query = """
        SELECT ?resource ?hasIdentifier ?implementsInterface
        WHERE { VALUES ?type {
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#ClassType>
            }
            ?resource rdf:type ?type . 
            ?resource SEON_code:hasIdentifier ?hasIdentifier .
            ?resource SEON_code:implementsInterface ?implementsInterface .
        }
    """
    create_implements_query_result = g.query(create_implements_query)
    # Construct the edges.
    for row in create_implements_query_result:
        edge = Edge(
            namespace_to_id(row["resource"]),
            namespace_to_id(row["implementsInterface"]),
            1,
            "specializes",
        )
        edge.add_property("specializationType", "implements")
        add_edge(edge)


def _create_edges_from_method_or_constructor_interactions(
    g: Graph,
    edge_name: str,
    method_or_constructor_interaction_rdf_predicate: str,
    interacted_thing_rdf_predicate: str,
):
    """
    Create edges from method or constructor interactions.

    Methods and Constructors interact with other methods, constructors, and fields. This function creates edges
    from these interactions. The created edges go from the class in which the method or constructor is defined to the
    class in which the thing interacted with is defined. The edge is labeled with the number of times the interaction
    occurs.

    """

    # Construct the query.
    query = f"""
        SELECT ?resource ?{method_or_constructor_interaction_rdf_predicate} ?isDeclaredMethodOf ?isDeclaredConstructorOf
        WHERE {{
            {{
                ?resource rdf:type <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#Method> .
                ?resource SEON_code:isDeclaredMethodOf ?isDeclaredMethodOf .
                ?resource SEON_code:{method_or_constructor_interaction_rdf_predicate} ?{method_or_constructor_interaction_rdf_predicate} . 
            }}
            UNION
            {{
                ?resource rdf:type <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#Constructor> .
                ?resource SEON_code:isDeclaredConstructorOf ?isDeclaredMethodOf .
                ?resource SEON_code:{method_or_constructor_interaction_rdf_predicate} ?{method_or_constructor_interaction_rdf_predicate} .
            }}
        }}
    """
    query_result = g.query(query)
    interactions_per_class = {}
    for row in query_result:
        containing_class_id = namespace_to_id(
            row["isDeclaredMethodOf"] or row["isDeclaredConstructorOf"]
        )
        interacted_thing = row[method_or_constructor_interaction_rdf_predicate]
        if containing_class_id not in interactions_per_class:
            interactions_per_class[containing_class_id] = {}
        if interacted_thing not in interactions_per_class[containing_class_id]:
            interactions_per_class[containing_class_id][interacted_thing] = 1
        else:
            interactions_per_class[containing_class_id][interacted_thing] += 1

    # For each interaction, query further information about the interacted thing and create an edge.
    for (
        containing_class_id,
        interacted_things,
    ) in interactions_per_class.items():
        for interacted_thing, count in interacted_things.items():
            interacted_thing_delcaration_query = f"""
                SELECT ?{interacted_thing_rdf_predicate}
                WHERE {{
                    <{interacted_thing}> SEON_code:{interacted_thing_rdf_predicate} ?{interacted_thing_rdf_predicate} .
                }}
            """
            interacted_thing_declaration_query_result = g.query(
                interacted_thing_delcaration_query
            )
            # Create the edge.
            for declaration_row in interacted_thing_declaration_query_result:
                accessed_class_id = namespace_to_id(
                    declaration_row[interacted_thing_rdf_predicate]
                )
                if accessed_class_id != containing_class_id:
                    edge = Edge(
                        containing_class_id, accessed_class_id, count, edge_name
                    )
                    add_edge(edge)


def create_accesses_edges(g: Graph):
    """ Create edges from a method or constructor to the fields it accesses."""

    _create_edges_from_method_or_constructor_interactions(
        g, "accesses", "accessesField", "isDeclaredFieldOf"
    )


def create_calls_edges(g: Graph):
    """ Create edges from a method or constructor to the methods it calls."""
    
    _create_edges_from_method_or_constructor_interactions(
        g, "calls", "invokesMethod", "isDeclaredMethodOf"
    )


def create_constructs_edges(g: Graph):
    """ Create edges from a method or constructor to the classes it constructs."""

    # Construct the edges from constructors to classes.
    _create_edges_from_method_or_constructor_interactions(
        g, "constructs", "invokesConstructor", "isDeclaredConstructorOf"
    )

    # Construct the query.
    create_constructs_query = """
        SELECT ?resource ?isDeclaredMethodOf ?isDeclaredConstructorOf ?instantiatesClass
        WHERE { VALUES ?type {
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#Method>
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#Constructor>
            }
            ?resource rdf:type ?type . 
            ?resource SEON_code:instantiatesClass ?instantiatesClass .
            OPTIONAL {
                ?resource SEON_code:isDeclaredMethodOf ?isDeclaredMethodOf .
            }  
            OPTIONAL {
                ?resource SEON_code:isDeclaredConstructorOf ?isDeclaredConstructorOf .
            } 
        }
    """
    create_constructs_query_result = g.query(create_constructs_query)
    # Construct the edges.
    for row in create_constructs_query_result:
        # If the resource is a method, create an edge from the method to the class it constructs.
        if row["isDeclaredMethodOf"]:
            edge = Edge(
                namespace_to_id(row["isDeclaredMethodOf"]),
                namespace_to_id(row["instantiatesClass"]),
                1,
                "constructs",
            )
            add_edge(edge)
        # If the resource is a constructor, create an edge from the constructor to the class it constructs.
        elif row["isDeclaredConstructorOf"]:
            edge = Edge(
                namespace_to_id(row["isDeclaredConstructorOf"]),
                namespace_to_id(row["instantiatesClass"]),
                1,
                "constructs",
            )
            add_edge(edge)



def create_holds_edges(g: Graph):
    """ Create edges from a field to the datatypes it holds."""

    # Construct the query.
    create_holds_query = """
        SELECT ?resource ?isDeclaredFieldOf ?hasDatatype
        WHERE {
            ?resource rdf:type <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#Field> .
            ?resource SEON_code:isDeclaredFieldOf ?isDeclaredFieldOf .
            ?resource SEON_code:hasDatatype ?hasDatatype .
        }
    """
    create_holds_query_result = g.query(create_holds_query)
    holds_data = {}
    for row in create_holds_query_result:
        source = namespace_to_id(row["isDeclaredFieldOf"])
        target = namespace_to_id(row["hasDatatype"])

        if source not in holds_data:
            holds_data[source] = {}
        if target not in holds_data[source]:
            holds_data[source][target] = 1
        else:
            holds_data[source][target] += 1

    # Construct the edges.
    for source, targets in holds_data.items():
        for target, count in targets.items():
            holds_edge = Edge(source, target, count, "holds")
            add_edge(holds_edge)


def create_accepts_edges(g: Graph):
    """ Create edges from a method or constructor to the datatypes it accepts as parameters."""

    # Construct the query.
    create_holds_query = """
        SELECT ?resource ?isParameterOf ?hasDatatype
        WHERE {
            ?resource rdf:type <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#Parameter> .
            ?resource SEON_code:isParameterOf ?isParameterOf .
            ?resource SEON_code:hasDatatype ?hasDatatype .
        }
    """
    create_holds_query_result = g.query(create_holds_query)
    accepts_data = {}

    # For each parameter, query further information about the datatype.
    for row in create_holds_query_result:
        isDeclaredMethodOf_query = f"""
            SELECT ?isDeclaredMethodOf
            WHERE {{
                <{row['isParameterOf']}> SEON_code:isDeclaredMethodOf ?isDeclaredMethodOf .
            }}
        """
        isDeclaredMethodOf_query_result = g.query(isDeclaredMethodOf_query)
        for isDeclaredMethodOf_row in isDeclaredMethodOf_query_result:
            source = namespace_to_id(isDeclaredMethodOf_row["isDeclaredMethodOf"])

        target = namespace_to_id(row["hasDatatype"])

        if source not in accepts_data:
            accepts_data[source] = {}
        if target not in accepts_data[source]:
            accepts_data[source][target] = 1
        else:
            accepts_data[source][target] += 1

    # Construct the edges.
    for source, targets in accepts_data.items():
        for target, count in targets.items():
            accepts_edge = Edge(source, target, count, "accepts")
            add_edge(accepts_edge)


def create_returns_edges(g: Graph):
    """ Create edges from a method to the datatypes it returns."""

    # Construct the query.
    create_holds_query = """
        SELECT ?resource ?isDeclaredMethodOf ?hasReturnType
        WHERE {
            ?resource rdf:type <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#Method> .
            ?resource SEON_code:isDeclaredMethodOf ?isDeclaredMethodOf .
            ?resource SEON_code:hasReturnType ?hasReturnType .
        }
    """
    create_holds_query_result = g.query(create_holds_query)
    returns_data = {}
    for row in create_holds_query_result:
        source = namespace_to_id(row["isDeclaredMethodOf"])
        target = namespace_to_id(row["hasReturnType"])

        if source not in returns_data:
            returns_data[source] = {}
        if target not in returns_data[source]:
            returns_data[source][target] = 1
        else:
            returns_data[source][target] += 1

    # Construct the edges.
    for source, targets in returns_data.items():
        for target, count in targets.items():
            returns_edge = Edge(source, target, count, "returns")
            add_edge(returns_edge)
