import subprocess
import webbrowser
import time
import threading

def run_backend():
    subprocess.Popen(["uvicorn", "core.api:app", "--reload", "--port", "8000"])
    
def run_frontend():
    subprocess.Popen(["python", "-m", "http.server", "3000"], cwd="pages")

def open_browser():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:3000/schedule.html")

if __name__ == "__main__":
    threading.Thread(target=run_backend, daemon=True).start()
    threading.Thread(target=run_frontend, daemon=True).start()
    open_browser()
