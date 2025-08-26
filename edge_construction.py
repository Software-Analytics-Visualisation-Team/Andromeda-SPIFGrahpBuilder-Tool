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
        source = ID_ALIAS.get(row["hasIdentifier"].toPython(), row["hasIdentifier"].toPython())
        target = ID_ALIAS.get(row["nestedIdentifier"].toPython(), row["nestedIdentifier"].toPython())
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
        SELECT ?sub_id ?sup_id
        WHERE {
            ?sub rdf:type <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#ClassType> .
            ?sub SEON_code:hasSuperClass ?sup .
            ?sub SEON_code:hasIdentifier ?sub_id .
            ?sup SEON_code:hasIdentifier ?sup_id .
        }
    """
    create_extends_query_result = g.query(create_extends_query)
    # Construct the edges.
    for row in create_extends_query_result:
        source = ID_ALIAS.get(row["sub_id"].toPython(), row["sub_id"].toPython())
        target = ID_ALIAS.get(row["sup_id"].toPython(), row["sup_id"].toPython())
        edge = Edge(source, target, 1, "specializes")
        edge.add_property("specializationType", "extends")
        add_edge(edge)

    # Construct the query.
    # For interfaces extending interfaces.
    create_extends_query = """
        SELECT ?sub_id ?sup_id
        WHERE { VALUES ?type {
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#InterfaceType>
            }
            ?sub rdf:type ?type .
            ?sub SEON_code:hasSuperInterface ?sup .
            ?sub SEON_code:hasIdentifier ?sub_id .
            ?sup SEON_code:hasIdentifier ?sup_id .
        }
    """
    create_extends_query_result = g.query(create_extends_query)
    # Construct the edges.
    for row in create_extends_query_result:
        source = ID_ALIAS.get(row["sub_id"].toPython(), row["sub_id"].toPython())
        target = ID_ALIAS.get(row["sup_id"].toPython(), row["sup_id"].toPython())
        edge = Edge(source, target, 1, "specializes")
        edge.add_property("specializationType", "extends")
        add_edge(edge)
        

def create_implements_edges(g: Graph):
    """ Create edges from a class to the interfaces it implements."""

    # Construct the query.
    create_implements_query = """
        SELECT ?cls_id ?itf_id
        WHERE {
            ?resource rdf:type <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#ClassType> .
            ?resource SEON_code:implementsInterface ?itf .
            ?resource SEON_code:hasIdentifier ?cls_id .
            ?itf SEON_code:hasIdentifier ?itf_id .
        }
    """
    create_implements_query_result = g.query(create_implements_query)
    # Construct the edges.
    for row in create_implements_query_result:
        source = ID_ALIAS.get(row["cls_id"].toPython(), row["cls_id"].toPython())
        target = ID_ALIAS.get(row["itf_id"].toPython(), row["itf_id"].toPython())
        edge = Edge(source, target, 1, "specializes")
        edge.add_property("specializationType", "implements")
        add_edge(edge)


def _create_edges_from_method_or_constructor_interactions(
    g: Graph,
    edge_name: str,
    method_or_constructor_interaction_rdf_predicate: str,
    interacted_thing_rdf_predicate: str,
):
    """
    Create edges from methods/constructors (declaring class) to the class that declares the interacted thing.
    """
    query = f"""
        SELECT ?declClass_id ?thing
        WHERE {{
            {{
                ?m rdf:type <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#Method> .
                ?m SEON_code:isDeclaredMethodOf ?cls .
                ?m SEON_code:{method_or_constructor_interaction_rdf_predicate} ?thing .
            }}
            UNION
            {{
                ?c rdf:type <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#Constructor> .
                ?c SEON_code:isDeclaredConstructorOf ?cls .
                ?c SEON_code:{method_or_constructor_interaction_rdf_predicate} ?thing .
            }}
            ?cls SEON_code:hasIdentifier ?declClass_id .
        }}
    """
    by_class = {}
    for row in g.query(query):
        source = ID_ALIAS.get(row["declClass_id"].toPython(), row["declClass_id"].toPython())
        thing = row["thing"]
        by_class.setdefault(source, {}).setdefault(thing, 0)
        by_class[source][thing] += 1

    for source, things in by_class.items():
        for thing, count in things.items():
            q2 = f"""
                SELECT ?decl_id
                WHERE {{
                    <{thing}> SEON_code:{interacted_thing_rdf_predicate} ?decl .
                    ?decl SEON_code:hasIdentifier ?decl_id .
                }}
            """
            for r2 in g.query(q2):
                target = ID_ALIAS.get(r2["decl_id"].toPython(), r2["decl_id"].toPython())
                if target != source:
                    edge = Edge(source, target, count, edge_name)
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
    """Create edges from methods/constructors to classes they construct."""
    _create_edges_from_method_or_constructor_interactions(
        g, "constructs", "invokesConstructor", "isDeclaredConstructorOf"
    )
    q = """
        SELECT ?declClass_id ?instCls_id
        WHERE {
            {
                ?m rdf:type <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#Method> .
                ?m SEON_code:isDeclaredMethodOf ?cls .
                ?m SEON_code:instantiatesClass ?instCls .
            }
            UNION
            {
                ?c rdf:type <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#Constructor> .
                ?c SEON_code:isDeclaredConstructorOf ?cls .
                ?c SEON_code:instantiatesClass ?instCls .
            }
            ?cls    SEON_code:hasIdentifier ?declClass_id .
            ?instCls SEON_code:hasIdentifier ?instCls_id .
        }
    """
    counts = {}
    for row in g.query(q):
        source = ID_ALIAS.get(row["declClass_id"].toPython(), row["declClass_id"].toPython())
        target = ID_ALIAS.get(row["instCls_id"].toPython(), row["instCls_id"].toPython())
        counts.setdefault(source, {}).setdefault(target, 0)
        counts[source][target] += 1
    for source, targets in counts.items():
        for target, c in targets.items():
            edge = Edge(source, target, c, "constructs")
            add_edge(edge)


def create_holds_edges(g: Graph):
    """Create edges from a field's declaring class to the datatype it holds."""
    q = """
        SELECT ?declClass_id ?dt_id
        WHERE {
            ?f rdf:type <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#Field> .
            ?f SEON_code:isDeclaredFieldOf ?cls .
            ?f SEON_code:hasDatatype ?dt .
            ?cls SEON_code:hasIdentifier ?declClass_id .
            ?dt  SEON_code:hasIdentifier ?dt_id .
        }
    """
    counts = {}
    for row in g.query(q):
        source = ID_ALIAS.get(row["declClass_id"].toPython(), row["declClass_id"].toPython())
        target = ID_ALIAS.get(row["dt_id"].toPython(), row["dt_id"].toPython())
        counts.setdefault(source, {}).setdefault(target, 0)
        counts[source][target] += 1
    for source, targets in counts.items():
        for target, c in targets.items():
            edge = Edge(source, target, c, "holds")
            add_edge(edge)


def create_accepts_edges(g: Graph):
    """Create edges from a method's declaring class to the parameter datatype it accepts."""
    q = """
        SELECT ?declClass_id ?dt_id
        WHERE {
            ?p rdf:type <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#Parameter> .
            ?p SEON_code:isParameterOf ?m .
            ?p SEON_code:hasDatatype ?dt .
            ?m SEON_code:isDeclaredMethodOf ?cls .
            ?cls SEON_code:hasIdentifier ?declClass_id .
            ?dt  SEON_code:hasIdentifier ?dt_id .
        }
    """
    counts = {}
    for row in g.query(q):
        source = ID_ALIAS.get(row["declClass_id"].toPython(), row["declClass_id"].toPython())
        target = ID_ALIAS.get(row["dt_id"].toPython(), row["dt_id"].toPython())
        counts.setdefault(source, {}).setdefault(target, 0)
        counts[source][target] += 1
    for source, targets in counts.items():
        for target, c in targets.items():
            edge = Edge(source, target, c, "accepts")
            add_edge(edge)


def create_returns_edges(g: Graph):
    """Create edges from a method's declaring class to the return datatype."""
    q = """
        SELECT ?declClass_id ?rt_id
        WHERE {
            ?m rdf:type <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#Method> .
            ?m SEON_code:isDeclaredMethodOf ?cls .
            ?m SEON_code:hasReturnType ?rt .
            ?cls SEON_code:hasIdentifier ?declClass_id .
            ?rt  SEON_code:hasIdentifier ?rt_id .
        }
    """
    counts = {}
    for row in g.query(q):
        source = ID_ALIAS.get(row["declClass_id"].toPython(), row["declClass_id"].toPython())
        target = ID_ALIAS.get(row["rt_id"].toPython(), row["rt_id"].toPython())
        counts.setdefault(source, {}).setdefault(target, 0)
        counts[source][target] += 1
    for source, targets in counts.items():
        for target, c in targets.items():
            edge = Edge(source, target, c, "returns")
            add_edge(edge)
