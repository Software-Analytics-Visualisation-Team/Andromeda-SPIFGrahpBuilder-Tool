import unittest
import rdflib
import graph_generator
import json_construction
import json
from deepdiff import DeepDiff


class TestJsonConstruction(unittest.TestCase):
    graph: rdflib.Graph

    def setUp(self):
        json_construction._edges = []
        self.graph = graph_generator.create_test_graph(create_nodes=True, create_edges=True)

    @classmethod
    def setUpClass(cls):
        print("""
        Started testing json_construction methods
        """)

    @classmethod
    def tearDownClass(cls):
        print("""
        Finished testing json_construction methods
        """)

    # Load JSON data from the test json
    with open("tests/expected_output.json", "r") as file:
        expected_json = json.load(file)

    def test_construct_json_from_nodes_and_edges(self):
        """
        Test construct_json_from_nodes_and_edges method
        """
        generated_json = json.loads(json_construction.construct_json_from_nodes_and_edges())
        diff = DeepDiff(self.expected_json, generated_json, ignore_order=True)
        self.assertTrue(not diff, "Incorrect JSON file generated.")


if __name__ == '__main__':
    unittest.main()
