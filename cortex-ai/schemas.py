from pydantic import BaseModel, Field
from enum import Enum
from typing import List

class Node(BaseModel):
    node_id: str = Field(description="A unique UUID for this node")
    content: str = Field(description="The content of the node")
    source: str = Field(description="Source of hthe node, e.g. Whatsapp, Telegram etc.")
    

class EdgeType(str, Enum):
    SUPPORTS = "SUPPORTS"
    CONTRADICTS = "CONTRADICTS"
    REQUIRES_CONTEXT = "REQUIRES_CONTEXT"
    BLOCKS = "BLOCKS"

class Edge(BaseModel):
    source_node_id: str = Field(description="The UUID of the source node")
    target_node_id: str = Field(description="The UUID of the destination node")
    relationship: EdgeType
    confidence_score: float = Field(description="A confidence score from 0.0 to 1.0 indicating how certain the AI is of this link.")

class KnowledgeGraph(BaseModel):
    nodes: list[Node]
    edges: list[Edge]

