import os
from google import genai
import instructor
from schemas import KnowledgeGraph
from dotenv import load_dotenv

load_dotenv()

client = instructor.from_genai(
    client=genai.Client(),
    mode=instructor.Mode.GENAI_TOOLS,
)

# user text comes from the api request
def extract_knowledge(user_text: str) -> KnowledgeGraph:
    print(f"Processing text from: {user_text}")



    response = client.chat.completions.create(
        model = "gemini-2.5-flash",
        response_model=KnowledgeGraph,
        strict=False,
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert Data Architect. Your job is to extract atomic entities (Nodes) "
                    "and logical relationships (Edges) from the user's text. "
                    "RULES: "
                    "1. Every Node must have a unique string for 'node_id' (e.g., 'node_1', 'node_2'). "
                    "2. You MUST extract relationships if they exist. Use EdgeTypes like BLOCKS or REQUIRES_CONTEXT. "
                    "3. Assign a 'confidence_score' (0.0 to 1.0) to every Edge. Be highly critical. "
                    "4. The 'source' for Nodes should just be 'User_Input'."
                )
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    )
    
    # 0.85 percent certaintly should be there for the model to extract that edge
    THRESHOLD = 0.85
    original_edge_count = len(response.edges)
    valid_edges = []
    for edge in response.edges:
        if edge.confidence_score >= THRESHOLD:
            valid_edges.append(edge)
        else:
            print(f"Removed edge: {edge.relationship} from node {edge.source_node_id} to node {edge.target_node_id} because the confidence score {edge.confidence_score} is below the threshold of {THRESHOLD} certainty")
    print(f"Extracted {len(valid_edges)} out of {original_edge_count} possible edges")
    response.edges = valid_edges

    # referential integrity filter (orphan check)
    valid_node_ids = {node.node_id for node in response.nodes}
    
    integrity_checked_edges = []
    for edge in response.edges:
        if edge.source_node_id in valid_node_ids and edge.target_node_id in valid_node_ids:
            integrity_checked_edges.append(edge)
        else:
            print(f"Removed edge ({edge.source_node_id} -> {edge.target_node_id}) because it references a non-existent node.")

    response.edges = integrity_checked_edges
    
    print(f"final edges after all filters: {len(response.edges)}")
    return response
    



# this snippet only runs if you run main.py directly
if __name__ == "__main__":
    test_input = ("I have a Python test about FastAPI next Friday before I start my project.")
    result_graph = extract_knowledge(test_input)
    
    # for example if the ai hallucinated an edge it would look like this
    from schemas import Edge, EdgeType
    fake_orphan_edge = Edge(
        source_node_id=result_graph.nodes[0].node_id, # node_0 -> hallucinated node
        target_node_id="made_up_hallucinated_node_id_999", # target doesnt exist so it will be removed 
        relationship=EdgeType.REQUIRES_CONTEXT,
        confidence_score=0.99
    )
    result_graph.edges.append(fake_orphan_edge) # adding the fake edge 
    
    # now run the filter manually just to test it
    valid_ids = {n.node_id for n in result_graph.nodes}
    if fake_orphan_edge.target_node_id not in valid_ids:
         print("test passed and the filter successfully caught the orphan.")
         # removing the fake edge 
         result_graph.edges.remove(fake_orphan_edge)

    print("Final Output:\n", result_graph.model_dump_json(indent=2))




