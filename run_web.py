import subprocess
import webbrowser
import time
import threading
import signal
import sys
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Глобальные переменные для хранения процессов
backend_process = None
frontend_process = None

def run_backend():
    global backend_process
    logger.info("Запуск backend (FastAPI)...")
    backend_process = subprocess.Popen(["uvicorn", "core.api:app", "--host", "127.0.0.1", "--port", "8000"])
    backend_process.wait()  # Блокируем поток до завершения процесса

def run_frontend():
    global frontend_process
    logger.info("Запуск фронтенда (HTTP-сервер)...")
    frontend_process = subprocess.Popen(["python", "-m", "http.server", "3000", "--bind", "127.0.0.1"], cwd="pages")
    frontend_process.wait()  # Блокируем поток до завершения процесса

def open_browser():
    logger.info("Открытие браузера...")
    time.sleep(2)  # Даём время на запуск серверов
    webbrowser.open("http://127.0.0.1:3000/schedule.html", 0)


def signal_handler(sig, frame):
    global backend_process, frontend_process
    logger.info("Получен сигнал прерывания. Завершение процессов...")
    
    if backend_process:
        logger.info("Остановка backend...")
        backend_process.terminate()
        try:
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()
            logger.warning("Backend принудительно завершён")
    
    if frontend_process:
        logger.info("Остановка фронтенда...")
        frontend_process.terminate()
        try:
            frontend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            frontend_process.kill()
            logger.warning("Фронтенд принудительно завершён")
    
    logger.info("Все процессы завершены. Выход...")
    sys.exit(0)

if __name__ == "__main__":
    # Установка обработчика сигнала
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Запуск процессов в потоках
    threading.Thread(target=run_backend, daemon=True).start()
    threading.Thread(target=run_frontend, daemon=True).start()
    open_browser()

    # Бесконечный цикл для предотвращения немедленного завершения main-потока
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)