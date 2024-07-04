import json


class Node:
    """ Node class for constructing JSON for Classviz. 
    
    Args:
        id (str): The unique identifier of the node.
        labels (list): The labels of the node.
        simpleName (str): The simple name of the node.
    
    """


    def __init__(self, id: str, labels: list, simpleName: str):
        """Initializes the Node object with the given parameters.
            Sets default value for metaSrc to "source code".
        """

        self.id = id
        self.labels = labels
        self.properties = {}
        self.add_property("simpleName", simpleName)
        self.add_property("metaSrc", "source code")

    def to_json(self) -> dict:
        """Converts the Node object to a JSON object."""

        data = {"id": self.id, "labels": self.labels, "properties": self.properties}
        return {"data": data}

    def add_property(self, key: str, value: str) -> None:
        """Adds a property to the Node object."""

        self.properties[key] = value


class Edge:

    """ Edge class for constructing JSON for Classviz.

    Args:
        source_id (str): The unique identifier of the source node.
        target_id (str): The unique identifier of the target node.
        weight (int): The weight of the edge.
        label (str): The label of the edge.
    
    """

    def __init__(self, source_id: str, target_id: str, weight: int, label: str):
        """Initializes the Edge object with the given parameters.
            Sets default value for metaSrc to "source code".
        """

        self.source_id = source_id
        self.target_id = target_id
        self.weight = weight
        self.label = label
        self.metaSrc = "source code"
        self.properties = {"weight": self.weight}

    def get_id(self) -> str:
        """Returns the unique identifier of the edge."""

        return f"{self.source_id}-{self.label}-{self.target_id}"

    def to_json(self) -> dict:
        """Converts the Edge object to a JSON object.
        
            The json contains the source, target, label, and properties of the edge.
        """

        data = {
            "id": self.get_id(),
            "source": self.source_id,
            "label": self.label,
            "properties": self.properties,
            "target": self.target_id,
        }
        return {"data": data}

    def add_property(self, key: str, value: str) -> None:
        """Adds a property to the Edge object."""

        self.properties[key] = value


_nodes = []
_edges = []


def construct_json_from_nodes_and_edges(pretty_print=True):
    """Constructs JSON from the nodes and edges.

    Args:
        pretty_print (bool): Whether to pretty print the JSON.

    Returns:
        str: The JSON constructed from the nodes and edges.

    """

    # Clean edges, such that there are no edges for which we do not have a source and target node.
    # Classviz does not handle these cases well.
    for edge in _edges:
        if edge.source_id not in [node.id for node in _nodes] or edge.target_id not in [node.id for node in _nodes]:
            print(f"Edge {edge.get_id()} has no source or target node. Removing it.")
            _edges.remove(edge)

    elements = {
        "nodes": [node.to_json() for node in _nodes],
        "edges": [edge.to_json() for edge in _edges],
    }
    return json.dumps({"elements": elements}, indent=(4 if pretty_print else 0))


def add_node(node: Node):
    """Adds a node to the list of nodes."""

    _nodes.append(node)


def add_edge(edge: Edge):
    """Adds an edge to the list of edges."""

    _edges.append(edge)
