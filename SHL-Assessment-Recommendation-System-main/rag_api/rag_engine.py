import os
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA


os.environ["GOOGLE_API_KEY"] = "AIzaSyAs0LwCSfSlECkmcYhVJ8r5sHYKcKNfX6E"

def get_rag_chain():
    
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    db = Chroma(
        persist_directory=r"C:\Users\hp\Downloads\SHL-Assessment-Recommendation-System-main\SHL-Assessment-Recommendation-System-main\chromadb", 
        embedding_function=embedding
    )
    
  
    retriever = db.as_retriever(search_kwargs={"k": 10})
    
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
    
    
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    
    return chain
