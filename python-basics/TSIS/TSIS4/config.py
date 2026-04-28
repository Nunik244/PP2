import json
import os

SETTINGS_FILE = 'settings.json'  # Имя файла для сохранения настроек

DEFAULT_SETTINGS = {
    "snake_color": [0, 255, 0],  # Цвет змейки (RGB: зеленый)
    "grid_overlay": True,         # Показывать сетку на поле
    "sound": True                 # Включить звук (заглушка для будущего)
}

def load_settings():
    """
    Загружает настройки из JSON файла.
    Если файла нет - создает его с настройками по умолчанию.
    Возвращает словарь с настройками.
    """
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)  # Создаем файл если его нет
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
            # Проверяем, что все ключи из DEFAULT_SETTINGS присутствуют
            for key in DEFAULT_SETTINGS:
                if key not in settings:
                    settings[key] = DEFAULT_SETTINGS[key]
            return settings
    except Exception as e:
        print(f"Error loading settings: {e}")
        return DEFAULT_SETTINGS.copy()

def save_settings(settings_dict):
    """
    Сохраняет настройки в JSON файл.
    Принимает словарь с настройками для сохранения.
    """
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings_dict, f, indent=4)  # indent=4 для читаемости
    except Exception as e:
        print(f"Error saving settings: {e}")