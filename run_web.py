import subprocess
import webbrowser
import time
import threading

def run_backend():
    subprocess.Popen(["uvicorn", "core.main:app", "--reload", "--port", "8000"])

def open_browser():
    time.sleep(2)
    webbrowser.open("http://localhost:5500/pages/Вебморда.html")  # или путь к вашей html

if __name__ == "__main__":
    threading.Thread(target=run_backend, daemon=True).start()
    open_browser()
