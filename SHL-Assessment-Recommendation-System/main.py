import subprocess
import time

def run_catalog_loader():
    subprocess.run(["python", "vector_store.py"])

def run_rag_engine():
    subprocess.run(["python", "rag_engine.py"])

def run_api_app():
    subprocess.Popen(["uvicorn", "api_app:app", "--reload"])

def run_streamlit_app():
    subprocess.run(["streamlit", "run", "streamlit_app.py"])

if __name__ == "__main__":
    run_catalog_loader()
    time.sleep(2)
    run_rag_engine()
    time.sleep(2)
    run_api_app()
    time.sleep(2)
    run_streamlit_app()
