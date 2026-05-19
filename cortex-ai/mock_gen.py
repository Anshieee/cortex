import json
from schemas import Edge, EdgeType, KnowledgeGraph, Node
import uuid

node1_id = str(uuid.uuid4())
node2_id = str(uuid.uuid4())

node1 = Node(node_id=node1_id, content="Learn React Hooks", source="Telegram")
node2 = Node(node_id=node2_id, content="React UI Project due Friday", source="Calendar")

edge = Edge(
    source_node_id=node1_id,
    target_node_id=node2_id,
    relationship=EdgeType.BLOCKS,
    confidence_score=0.95
)

kg = KnowledgeGraph(nodes=[node1, node2], edges=[edge])


with open("mock_kg.json", "w") as f:
    json.dump(kg.model_dump(), f, indent=2)

