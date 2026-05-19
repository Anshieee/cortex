from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import extract_knowledge
from pydantic import parse_obj_as
import jsonref

app = FastAPI()

class ExtractionRequest(BaseModel):
    text: str

# post request to extract graph
@app.post("/extract")
async def extract_graph(request: ExtractionRequest):
    try:
        graph = extract_knowledge(request.text)
        return graph
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# check health (apparently its a good habit)
@app.get("/health")
async def health_check():
    return {"status": "ok"}

