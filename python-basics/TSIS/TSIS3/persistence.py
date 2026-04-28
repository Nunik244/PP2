import json
import os

def load_json(filename, default):
    """Загружает данные из JSON файла"""
    if not os.path.exists(filename):
        return default
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return default

def save_json(filename, data):
    """Сохраняет данные в JSON файл"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def get_leaderboard():
    """Возвращает таблицу рекордов"""
    return load_json('leaderboard.json', [])

def save_score(name, score, distance):
    """Сохраняет результат игрока"""
    data = get_leaderboard()
    data.append({"name": name, "score": score, "distance": distance})
    # Сортируем по убыванию очков
    data = sorted(data, key=lambda x: x['score'], reverse=True)[:10]
    save_json('leaderboard.json', data)

def get_settings():
    """Загружает настройки игры"""
    default = {
        "sound": True, 
        "car_color": [255, 0, 0], 
        "difficulty": "Medium"
    }
    settings = load_json('settings.json', default)
    # Проверяем, что все ключи есть
    for key in default:
        if key not in settings:
            settings[key] = default[key]
    return settings

def save_settings(settings):
    """Сохраняет настройки игры"""
    save_json('settings.json', settings)