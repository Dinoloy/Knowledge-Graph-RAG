
import networkx as nx

GRAPH_FILE = "schemes_knowledge_graph.graphml"

graph = nx.read_graphml(GRAPH_FILE)

print("Knowledge Graph loaded successfully!")
print(f"Nodes: {graph.number_of_nodes()}")
print(f"Edges: {graph.number_of_edges()}")

print("\nSearching for 'Training to Farmers':")

for node, data in graph.nodes(data=True):
    if (
        data.get("entity_type") == "Scheme"
        and "training to farmers" in data.get("name", "").lower()
    ):
        print("\nScheme:", data["name"])
        print("URL:", data.get("url", ""))
        print("Department:", data.get("funding_pattern", ""))

        print("Relationships:")
        for _, target, edge_data in graph.out_edges(node, data=True):
            target_data = graph.nodes[target]
            print(
                f"  --{edge_data.get('relation')}--> "
                f"{target_data.get('name', target)}"
            )
