import os
import sys
import requests
import time
from packaging import version

# Конфигурация
REPO_URL = "https://api.github.com/repos/ваш-username/ваш-репозиторий/releases/latest"
CURRENT_VERSION = "1.0.0"  # Текущая версия программы
SCRIPT_NAME = "main.py"    # Имя файла для обновления

def check_for_updates():
    try:
        response = requests.get(REPO_URL)
        if response.status_code == 200:
            latest_release = response.json()
            latest_version = latest_release["tag_name"]
            
            if version.parse(latest_version) > version.parse(CURRENT_VERSION):
                print(f"Найдена новая версия: {latest_version}")
                return True, latest_release["assets"][0]["browser_download_url"]
        else:
            print("Не удалось проверить обновления.")
    except Exception as e:
        print(f"Ошибка при проверке обновлений: {e}")
    return False, None

def download_update(download_url):
    try:
        print("Скачивание обновления...")
        response = requests.get(download_url)
        with open(SCRIPT_NAME, "wb") as file:
            file.write(response.content)
        print("Обновление успешно загружено!")
        return True
    except Exception as e:
        print(f"Ошибка при скачивании: {e}")
        return False

def restart_program():
    print("Перезапуск программы...")
    time.sleep(2)
    os.execv(sys.executable, [sys.executable, SCRIPT_NAME])

def main():
    print(f"Текущая версия: {CURRENT_VERSION}")
    update_available, download_url = check_for_updates()
    
    if update_available:
        if download_update(download_url):
            restart_program()
    
    # Основная логика программы
    print("Программа работает...")
    time.sleep(5)

if __name__ == "__main__":
    main()