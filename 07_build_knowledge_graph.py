
import json
import networkx as nx

INPUT_FILE = "schemes_details.json"
OUTPUT_FILE = "schemes_knowledge_graph.graphml"
SUMMARY_FILE = "knowledge_graph_summary.json"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    schemes = json.load(file)

graph = nx.MultiDiGraph()


def add_entity(entity_type, name):
    name = name.strip()
    if not name:
        return None

    node_id = f"{entity_type}::{name}"
    graph.add_node(node_id, entity_type=entity_type, name=name)
    return node_id


def connect(source, target, relation):
    if source and target:
        graph.add_edge(source, target, relation=relation)


for record in schemes:
    details = record.get("details", {})
    scheme_name = record.get("scheme_name", "").strip()

    if not scheme_name:
        continue

    scheme = add_entity("Scheme", scheme_name)

    graph.nodes[scheme]["url"] = record.get("url", "")
    graph.nodes[scheme]["funding_pattern"] = details.get("Funding Pattern", "")
    graph.nodes[scheme]["description"] = details.get("Description", "")
    graph.nodes[scheme]["eligibility_criteria"] = details.get(
        "Eligibility criteria", ""
    )
    graph.nodes[scheme]["how_to_avail"] = details.get("How To avail", "")

    department = add_entity(
        "Department", details.get("Concerned Department", "")
    )
    connect(scheme, department, "managed_by")

    beneficiaries = details.get("Beneficiaries", "")
    for beneficiary in beneficiaries.splitlines():
        node = add_entity("Beneficiary", beneficiary)
        connect(scheme, node, "available_to")

    benefit_types = details.get("Types of Benefits", "")
    for benefit in benefit_types.splitlines():
        node = add_entity("BenefitType", benefit)
        connect(scheme, node, "provides")

    sponsor = add_entity("Sponsor", details.get("Sponsered By", ""))
    connect(scheme, sponsor, "sponsored_by")

    application = details.get("How To avail", "")
    if application:
        method = add_entity("ApplicationMethod", application)
        connect(scheme, method, "application_process")


# Save the graph in a portable format
nx.write_graphml(graph, OUTPUT_FILE)

summary = {
    "scheme_records": len(schemes),
    "graph_nodes": graph.number_of_nodes(),
    "graph_edges": graph.number_of_edges(),
    "node_types": {},
    "relationship_types": {},
}

for _, attributes in graph.nodes(data=True):
    entity_type = attributes.get("entity_type", "Unknown")
    summary["node_types"][entity_type] = (
        summary["node_types"].get(entity_type, 0) + 1
    )

for _, _, attributes in graph.edges(data=True):
    relation = attributes.get("relation", "Unknown")
    summary["relationship_types"][relation] = (
        summary["relationship_types"].get(relation, 0) + 1
    )

with open(SUMMARY_FILE, "w", encoding="utf-8") as file:
    json.dump(summary, file, ensure_ascii=False, indent=2)

print("Knowledge Graph created successfully!")
print(json.dumps(summary, ensure_ascii=False, indent=2))
print(f"\nGraph saved to: {OUTPUT_FILE}")
print(f"Summary saved to: {SUMMARY_FILE}")
