from rdflib import Graph
from helpers import namespace_to_name, type_to_kind
from json_construction import Node, add_node


def create_primitive_nodes(g: Graph):
    """Creates nodes for the primitive types in the graph."""

    # Construct the query
    create_primitive_query = """
        SELECT ?hasCodeIdentifier ?hasIdentifier
        WHERE {
            ?hasCodeIdentifier rdf:type <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#PrimitiveType> .
            ?hasCodeIdentifier SEON_code:hasIdentifier ?hasIdentifier .
        }"""
    create_primitive_query_result = g.query(create_primitive_query)
    # Create a node for each primitive type
    for row in create_primitive_query_result:
        primitive = namespace_to_name(row["hasCodeIdentifier"])
        node = Node(row["hasIdentifier"].toPython(), ["Primitive"], primitive)
        add_node(node)


def create_container_nodes(g: Graph):
    """Creates nodes for the containers in the graph."""

    # Construct the query
    create_container_query = """
        SELECT ?hasCodeIdentifier ?hasIdentifier
        WHERE {
            ?hasCodeIdentifier rdf:type <http://se-on.org/ontologies/system-specific/2012/02/java.owl#JavaPackage> .
            ?hasCodeIdentifier SEON_code:hasIdentifier ?hasIdentifier .
        }"""
    create_container_query_result = g.query(create_container_query)
    # Create a node for each container
    for row in create_container_query_result:
        name = namespace_to_name(row["hasCodeIdentifier"])
        id = row["hasIdentifier"].toPython()
        node = Node(id, ["Container"], name)
        node.add_property("kind", "package")
        add_node(node)


def create_structure_nodes(g: Graph):
    """Creates nodes for the structures in the graph."""

    # Construct the query
    create_structure_query = """
        SELECT ?resource ?type ?hasCodeIdentifier ?hasIdentifier ?isAbstract ?isStaticComplexType ?hasAccessModifier
        WHERE { VALUES ?type {
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#ClassType>
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#EnumerationType>
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#InterfaceType>
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#Datatype>
                <http://se-on.org/ontologies/domain-specific/2012/02/code.owl#ExceptionType>
            } ?resource rdf:type ?type .
            ?resource SEON_code:hasCodeIdentifier ?hasCodeIdentifier .   
            ?resource SEON_code:hasIdentifier ?hasIdentifier .
            OPTIONAL {
                ?resource SEON_code:isAbstract ?isAbstract .
            }        
            OPTIONAL {
                ?resource ns1:isStaticComplexType ?isStaticComplexType .
            }
            OPTIONAL {
                ?resource SEON_code:hasAccessModifier ?hasAccessModifier .
            }
        }
    """
    create_structure_query_result = g.query(create_structure_query)
    # Create a node for each structure
    for row in create_structure_query_result:
        name = namespace_to_name(row["hasCodeIdentifier"])
        id = row["hasIdentifier"].toPython()
        node = Node(id, ["Structure"], name)
        # Add properties to the node
        node.add_property("kind", type_to_kind(row["type"], row["isAbstract"]))
        node.add_property(
            "isPublic",
            row["hasAccessModifier"] and "public" in row["hasAccessModifier"],
        )
        node.add_property("isClass", "ClassType" in row["type"])
        node.add_property("isInterface", "InterfaceType" in row["type"])
        if row["isAbstract"] != None:
            node.add_property("isAbstract", row["isAbstract"].toPython())
        node.add_property("isEnum", "EnumerationType" in row["type"])
        if row["isStaticComplexType"] != None:
            node.add_property("isStatic", row["isStaticComplexType"].toPython())
        add_node(node)
