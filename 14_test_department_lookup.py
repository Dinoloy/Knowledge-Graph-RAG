
import networkx as nx

GRAPH_FILE = "schemes_knowledge_graph.graphml"

graph = nx.read_graphml(GRAPH_FILE)

department_name = "Agriculture - Farmers Welfare Department"

# Find the department node using the actual graph attribute
department_nodes = [
    (node_id, data)
    for node_id, data in graph.nodes(data=True)
    if data.get("entity_type") == "Department"
    and data.get("name", "").strip().lower()
    == department_name.lower()
]

if not department_nodes:
    print(f"Department not found: {department_name}")
else:
    department_id, department_data = department_nodes[0]

    print(f"Department: {department_data.get('name')}")
    print("\nSchemes linked to this department:\n")

    schemes = []

    # Scheme -> Department edges point INTO the department node
    for source_id, _, edge_data in graph.in_edges(
        department_id, data=True
    ):
        source_data = graph.nodes[source_id]

        if source_data.get("entity_type") == "Scheme":
            schemes.append({
                "name": source_data.get("name", "Unknown"),
                "url": source_data.get("url", ""),
            })

    schemes.sort(key=lambda item: item["name"].lower())

    for index, scheme in enumerate(schemes, start=1):
        print(f"{index}. {scheme['name']}")
        if scheme["url"]:
            print(f"   Source: {scheme['url']}")

    print(f"\nTotal linked schemes: {len(schemes)}")
