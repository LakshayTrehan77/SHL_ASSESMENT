import os
import subprocess

# Run vector_store.py and Django server in one terminal
subprocess.run(["python", "vector_store.py"])
os.chdir("rag_api")
subprocess.run(["python", "manage.py", "runserver" , "--noreload"])

