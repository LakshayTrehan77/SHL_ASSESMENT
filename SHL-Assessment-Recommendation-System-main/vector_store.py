import json
import os


from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document


os.environ["GOOGLE_API_KEY"] = "AIzaSyAs0LwCSfSlECkmcYhVJ8r5sHYKcKNfX6E"


with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


docs = [
    Document(
        page_content=item["description"],
        metadata={
            "name": item.get("name", ""),
            "url": item.get("url", ""),
            "test_type": ", ".join(item.get("test_type", [])) if isinstance(item.get("test_type", []), list) else item.get("test_type", ""),
            "duration": item.get("duration", 0),
            "remote_support": item.get("remote_support", ""),
            "adaptive_support": item.get("adaptive_support", "")
        }
    )
    for item in catalog
]


embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


db = Chroma.from_documents(
    documents=docs,
    embedding=embedding,
    persist_directory="./chromadb"
)
db.persist()

print(f"✅ Stored {len(docs)} documents into Chroma DB at './chromadb'.")
