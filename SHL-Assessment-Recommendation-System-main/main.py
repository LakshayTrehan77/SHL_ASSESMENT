import os
import subprocess

# Run vector_store.py
subprocess.run(["python", "vector_store.py"])
# Change directory to rag_api and run Django server on 0.0.0.0:8080
os.chdir("rag_api")
subprocess.run(["python", "manage.py", "runserver", "0.0.0.0:8080", "--noreload"])
