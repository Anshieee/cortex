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
    return response
    



# this snippet only runs if you run main.py directly
if __name__ == "__main__":
    test_input = ("I have a Python test about FastAPI next Friday before I start my project.")
    result_graph = extract_knowledge(test_input)
    print("Final JSON: ", result_graph.model_dump_json(indent=2))




