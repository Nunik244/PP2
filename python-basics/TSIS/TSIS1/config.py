import os
from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    # Проверка, существует ли файл вообще
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл конфигурации {filename} не найден!")

    parser = ConfigParser()
    parser.read(filename)
    
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f'Секция {section} не найдена в файле {filename}')
    return config