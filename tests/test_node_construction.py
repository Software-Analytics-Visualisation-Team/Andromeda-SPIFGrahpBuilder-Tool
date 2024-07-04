import unittest
import rdflib
import graph_generator
import node_construction
import json_construction


class TestNodeConstruction(unittest.TestCase):
    graph: rdflib.Graph

    def setUp(self):
        json_construction._nodes = []
        self.graph = graph_generator.create_test_graph()

    @classmethod
    def setUpClass(cls):
        print("""
        Started testing node_construction methods
        """)

    @classmethod
    def tearDownClass(cls):
        print("""
        Finished testing node_construction methods
        """)

    def test_create_primitive_nodes(self):
        """
        Test create_primitive_nodes method
        """
        node_construction.create_primitive_nodes(self.graph)
        self.assertEqual(len(json_construction._nodes), 25, "Wrong amount of nodes created.")

        # Check if a specific primitive node exists
        sample_node = {
            'data': {
                'id': '4A594698_EF97_41B6_BD81_9B14DA153029',
                'labels': ['Primitive'],
                'properties': {
                    'simpleName': 'boolean',
                    'metaSrc': 'source code'
                }
            }
        }
        self.assertNodeInJson(sample_node)

    def test_create_container_nodes(self):
        """
        Test create_container_nodes method
        """
        node_construction.create_container_nodes(self.graph)
        self.assertEqual(len(json_construction._nodes), 2, "Wrong amount of nodes created.")

        # Check if a specific container node exists
        sample_node = {
            'data': {
                'id': '2_0_79172081851553355288295596375460223421075799440627657615203299781126254616016',
                'labels': ['Container'],
                'properties': {
                    'simpleName': 'testpackage',
                    'metaSrc': 'source code',
                    'kind': 'package'
                }
            }
        }
        self.assertNodeInJson(sample_node)

    def test_create_structure_nodes(self):
        """
        Test create_structure_nodes method
        """
        node_construction.create_structure_nodes(self.graph)
        self.assertEqual(len(json_construction._nodes), 28, "Wrong amount of nodes created.")

        # Check if a specific structure node exists
        sample_node = {
            'data': {
                'id': '72_10_7369412547006914277577921264035919370618363903026817757352188121963325577595',
                'labels': ['Structure'],
                'properties': {
                    'simpleName': 'Inner',
                    'metaSrc': 'source code',
                    'kind': 'class',
                    'isPublic': True,
                    'isClass': True,
                    'isInterface': False,
                    'isAbstract': False,
                    'isEnum': False
                }
            }
        }
        self.assertNodeInJson(sample_node)

    def assertNodeInJson(self, sample_node):
        nodes = { "nodes": [node.to_json() for node in json_construction._nodes] }
        self.assertTrue(sample_node in nodes["nodes"], "Expected node doesn't exist")


if __name__ == '__main__':
    unittest.main()
