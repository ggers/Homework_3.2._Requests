import requests
import chardet
import os

def translate_it(text, lang="ru"):
    """
    YANDEX translation plugin

    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/

    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :param text: <str> text for translation.
    :return: <str> translated text.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20180715T203220Z.ada27d4b85b556ee.4d6b5a9bce7f6c21d84f0fb076f06991e50f782e'

    params = {
        'key': key,
        'lang': lang,
        'text': text,
    }
    response = requests.get(url, params=params).json()
    return ' '.join(response.get('text', []))

def open_file_txt(target_file):
    encode = None
    strings = None
    with open(target_file, "rb") as txt_file:
        raw_info = txt_file.read()
        encode = chardet.detect(raw_info)
        strings = raw_info.decode(encode["encoding"])
    return strings

def create_file_txt(target_file, text):
    with open(target_file, "w") as txt_file:
        txt_file.write(text + '\n')

def create_subdirectory(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        print(f"Целевая директория {dirname} создана")

def get_files_from_directory(dir_name, file_type=".txt"):
    return [x for x in os.listdir(os.path.join(current_dir, dir_name)) if x.endswith(file_type)]

current_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    from_dir = input(f'Введите адрес исходной директории, Пробел для перевода из текущей директории {current_dir}\n')
    if from_dir == " ":
        from_dir = current_dir
        print(f"Начинаем перевод файлов в директории {from_dir}")
    else:
        print(f"Начинаем перевод файлов в директории {from_dir}")
    file_list = get_files_from_directory(from_dir)
    print(f"В данной директории присутствуют следующие файлы: {file_list}")
    from_file = input('Введите имя целевого файла\n')
    to_dir = input(f'Введите адрес целевой директории, Пробел для содания субдиректории "Result" в текущей лиректории {current_dir}\n')
    from_lang = input(f'Введите язык исходного файла:\n')
    to_lang = input(f'Введите язык целевого файла:\n')
    if to_dir == " ":
        to_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Result")
        print(f"Начинаем создание файлов в директории {to_dir}")
    else:
        print(f"Начинаем создание файлов в директории {to_dir}")
    create_subdirectory(to_dir)
    create_file_txt(os.path.join(to_dir, from_file), translate_it(open_file_txt(os.path.join(from_dir, from_file)), from_lang + "-" + to_lang))
    print("Проверяем содержимое получившегося файла\n", open_file_txt(os.path.join(to_dir, from_file)))
