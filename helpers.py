import urllib.parse

def namespace_to_name(uri):
    """Extracts the name of the namespace from the URI"""

    return urllib.parse.unquote(str((uri.split("#")[-1]).split("_")[0]))


def namespace_to_id(uri):
    """Extracts the ID of the namespace from the URI"""

    return str((uri.split("#")[-1]).split("_", 1)[-1])


def type_to_kind(type: str, isAbstract: bool = False):
    """Converts the type of the element to the kind of the element"""

    if isAbstract:
        return "abstract class"
    return {
        "ClassType": "class",
        "EnumerationType": "enum",
        "InterfaceType": "interface",
        "Method": "method",
        "Datatype": "imported",
        "ExceptionType": "exception",	
    }[type.split("#")[-1]]
