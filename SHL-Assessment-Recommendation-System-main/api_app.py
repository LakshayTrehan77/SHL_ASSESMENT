from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from rag_engine import get_rag_chain

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


rag_chain = get_rag_chain()

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/recommend")
async def recommend(request: Request):
    data = await request.json()
    query = data.get("query", "")
    try:
        result = rag_chain.run(query)
        return {
            "recommended_assessments": rag_chain.retriever.get_relevant_documents(query)
        }
    except Exception as e:
        print(f"Error in recommendation: {str(e)}")
        return {"error": "Error fetching recommendations. Please try again later."}
