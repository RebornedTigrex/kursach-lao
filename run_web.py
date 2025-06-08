import subprocess
import webbrowser
import time
import threading

def run_backend():
    subprocess.Popen(["uvicorn", "core.api:app", "--reload", "--port", "8000"])

def open_browser():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:3000/pages/schedule.html")  # или путь к вашей html

if __name__ == "__main__":
    threading.Thread(target=run_backend, daemon=True).start()
    open_browser()
