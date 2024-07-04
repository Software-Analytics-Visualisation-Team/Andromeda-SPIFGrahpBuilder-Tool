import unittest
import rdflib
import graph_generator
import edge_construction
import json_construction


class TestEdgeConstruction(unittest.TestCase):
    graph: rdflib.Graph

    def setUp(self):
        json_construction._edges = []
        self.graph = graph_generator.create_test_graph(create_nodes=True)

    @classmethod
    def setUpClass(cls):
        print("""
        Started testing edge_construction methods
        """)

    @classmethod
    def tearDownClass(cls):
        print("""
        Finished testing edge_construction methods
        """)

    def test_create_container_contains_container_edges(self):
        """
        Test create_container_contains_container_edges method
        """
        edge_construction.create_container_contains_container_edges(self.graph)
        self.assertEqual(len(json_construction._edges), 1, "Wrong amount of edges created.")

        sample_edge = {
            "data": {
                    "id": "2_0_79172081851553355288295596375460223421075799440627657615203299781126254616016-contains-2_0_34083927285473295706624098219623591006442775957558420822958356197242916605621",
                    "source": "2_0_79172081851553355288295596375460223421075799440627657615203299781126254616016",
                    "label": "contains",
                    "properties": {
                        "weight": 1
                    },
                    "target": "2_0_34083927285473295706624098219623591006442775957558420822958356197242916605621"
                }
        }
        self.assertEdgeInJson(sample_edge)

    def test_create_container_contains_structure_edges(self):
        """
        Test create_container_contains_structure_edges method
        """
        edge_construction.create_container_contains_structure_edges(self.graph)
        self.assertEqual(len(json_construction._edges), 1, "Wrong amount of edges created.")

        sample_edge = {
            "data": {
                    "id": "2_0_79172081851553355288295596375460223421075799440627657615203299781126254616016-contains-5_13_79172081851553355288295596375460223421075799440627657615203299781126254616016",
                    "source": "2_0_79172081851553355288295596375460223421075799440627657615203299781126254616016",
                    "label": "contains",
                    "properties": {
                        "weight": 1,
                        "containmentType": "package"
                    },
                    "target": "5_13_79172081851553355288295596375460223421075799440627657615203299781126254616016"
                }
        }
        self.assertEdgeInJson(sample_edge)

    def test_create_structure_contains_structure_edges(self):
        """
        Test create_structure_contains_structure_edges method
        """
        edge_construction.create_structure_contains_structure_edges(self.graph)
        self.assertEqual(len(json_construction._edges), 3, "Wrong amount of edges created.")

        sample_edge = {
            "data": {
                    "id": "95_13_75256506093048495533171443210287212606443336598199685019880837275799160799543-contains-124_9_75256506093048495533171443210287212606443336598199685019880837275799160799543",
                    "source": "95_13_75256506093048495533171443210287212606443336598199685019880837275799160799543",
                    "label": "contains",
                    "properties": {
                        "weight": 1,
                        "containmentType": "nested class"
                    },
                    "target": "124_9_75256506093048495533171443210287212606443336598199685019880837275799160799543"
                }
        }
        self.assertEdgeInJson(sample_edge)

    def test_create_extends_edges(self):
        """
        Test create_extends_edges method
        """
        edge_construction.create_extends_edges(self.graph)
        self.assertEqual(len(json_construction._edges), 3, "Wrong amount of edges created.")

        sample_edge = {
            "data": {
                    "id": "41_6_7369412547006914277577921264035919370618363903026817757352188121963325577595-specializes-33_6_7369412547006914277577921264035919370618363903026817757352188121963325577595",
                    "source": "41_6_7369412547006914277577921264035919370618363903026817757352188121963325577595",
                    "label": "specializes",
                    "properties": {
                        "weight": 1,
                        "specializationType": "extends"
                    },
                    "target": "33_6_7369412547006914277577921264035919370618363903026817757352188121963325577595"
                }
        }
        self.assertEdgeInJson(sample_edge)

    def test_create_implements_edges(self):
        """
        Test create_implements_edges method
        """
        edge_construction.create_implements_edges(self.graph)
        self.assertEqual(len(json_construction._edges), 2, "Wrong amount of edges created.")

        sample_edge = {
            "data": {
                    "id": "65_6_75256506093048495533171443210287212606443336598199685019880837275799160799543-specializes-60_10_75256506093048495533171443210287212606443336598199685019880837275799160799543",
                    "source": "65_6_75256506093048495533171443210287212606443336598199685019880837275799160799543",
                    "label": "specializes",
                    "properties": {
                        "weight": 1,
                        "specializationType": "implements"
                    },
                    "target": "60_10_75256506093048495533171443210287212606443336598199685019880837275799160799543"
                }
        }
        self.assertEdgeInJson(sample_edge)

    def test_create_accesses_edges(self):
        """
        Test create_accesses_edges method
        """
        edge_construction.create_accesses_edges(self.graph)
        self.assertEqual(len(json_construction._edges), 1, "Wrong amount of edges created.")

        sample_edge = {
            "data": {
                    "id": "8_13_34083927285473295706624098219623591006442775957558420822958356197242916605621-accesses-4_13_34083927285473295706624098219623591006442775957558420822958356197242916605621",
                    "source": "8_13_34083927285473295706624098219623591006442775957558420822958356197242916605621",
                    "label": "accesses",
                    "properties": {
                        "weight": 1
                    },
                    "target": "4_13_34083927285473295706624098219623591006442775957558420822958356197242916605621"
                }
        }
        self.assertEdgeInJson(sample_edge)

    def test_create_calls_edges(self):
        """
        Test create_calls_edges method
        """
        edge_construction.create_calls_edges(self.graph)
        self.assertEqual(len(json_construction._edges), 5, "Wrong amount of edges created.")

        sample_edge = {
            "data": {
                    "id": "95_13_75256506093048495533171443210287212606443336598199685019880837275799160799543-calls-134_17_75256506093048495533171443210287212606443336598199685019880837275799160799543",
                    "source": "95_13_75256506093048495533171443210287212606443336598199685019880837275799160799543",
                    "label": "calls",
                    "properties": {
                        "weight": 1
                    },
                    "target": "134_17_75256506093048495533171443210287212606443336598199685019880837275799160799543"
                }
        }
        self.assertEdgeInJson(sample_edge)

    def test_create_constructs_edges(self):
        """
        Test create_constructs_edges method
        """
        edge_construction.create_constructs_edges(self.graph)
        self.assertEqual(len(json_construction._edges), 8, "Wrong amount of edges created.")

        sample_edge_method = {
            "data": {
                    "id": "95_13_75256506093048495533171443210287212606443336598199685019880837275799160799543-constructs-95_13_75256506093048495533171443210287212606443336598199685019880837275799160799543",
                    "source": "95_13_75256506093048495533171443210287212606443336598199685019880837275799160799543",
                    "label": "constructs",
                    "properties": {
                        "weight": 1
                    },
                    "target": "95_13_75256506093048495533171443210287212606443336598199685019880837275799160799543"
                }
        }
        sample_edge_constructor = {
            "data": {
                    "id": "41_6_7369412547006914277577921264035919370618363903026817757352188121963325577595-constructs-5_13_79172081851553355288295596375460223421075799440627657615203299781126254616016",
                    "source": "41_6_7369412547006914277577921264035919370618363903026817757352188121963325577595",
                    "label": "constructs",
                    "properties": {
                        "weight": 1
                    },
                    "target": "5_13_79172081851553355288295596375460223421075799440627657615203299781126254616016"
                }
        }
        self.assertEdgeInJson(sample_edge_method)
        self.assertEdgeInJson(sample_edge_constructor)

    def test_create_holds_edges(self):
        """
        Test create_holds_edges method
        """
        edge_construction.create_holds_edges(self.graph)
        self.assertEqual(len(json_construction._edges), 4, "Wrong amount of edges created.")

        sample_edge = {
            "data": {
                    "id": "95_13_75256506093048495533171443210287212606443336598199685019880837275799160799543-holds-47_19_9547014781282255098475443303543643561754473281808646487758370679850828918066",
                    "source": "95_13_75256506093048495533171443210287212606443336598199685019880837275799160799543",
                    "label": "holds",
                    "properties": {
                        "weight": 1
                    },
                    "target": "47_19_9547014781282255098475443303543643561754473281808646487758370679850828918066"
                }
        }
        self.assertEdgeInJson(sample_edge)

    def test_create_accepts_edges(self):
        """
        Test create_accepts_edges method
        """
        edge_construction.create_accepts_edges(self.graph)
        self.assertEqual(len(json_construction._edges), 5, "Wrong amount of edges created.")

        sample_edge = {
            "data": {
                    "id": "29_6_75256506093048495533171443210287212606443336598199685019880837275799160799543-accepts-B4074745_3F53_4483_81A8_7CC032FCED2B",
                    "source": "29_6_75256506093048495533171443210287212606443336598199685019880837275799160799543",
                    "label": "accepts",
                    "properties": {
                        "weight": 8
                    },
                    "target": "B4074745_3F53_4483_81A8_7CC032FCED2B"
                }
        }
        self.assertEdgeInJson(sample_edge)

    def test_create_returns_edges(self):
        """
        Test create_returns_edges method
        """
        edge_construction.create_returns_edges(self.graph)
        self.assertEqual(len(json_construction._edges), 6, "Wrong amount of edges created.")

        sample_edge = {
            "data": {
                    "id": "51_6_75256506093048495533171443210287212606443336598199685019880837275799160799543-returns-B4074745_3F53_4483_81A8_7CC032FCED2B",
                    "source": "51_6_75256506093048495533171443210287212606443336598199685019880837275799160799543",
                    "label": "returns",
                    "properties": {
                        "weight": 1
                    },
                    "target": "B4074745_3F53_4483_81A8_7CC032FCED2B"
                }
        }
        self.assertEdgeInJson(sample_edge)

    def assertEdgeInJson(self, sample_edge):
        """
        Check if expected or unexpected edges are present in the generated JSON
        """
        edges = { "edges": [edge.to_json() for edge in json_construction._edges] }
        self.assertTrue(sample_edge in edges["edges"], "Expected edge doesn't exist")


if __name__ == '__main__':
    unittest.main()
