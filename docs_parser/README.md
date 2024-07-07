# Docs parser

Парсер документации [RuStore](https://www.rustore.ru/help/).

## Как работает

Берет все страницы из `sitemap.xml` и собирает (`main.py`).

На момент хакатона `Количество страниц документации: 479`.

Извлечение уникальных ссылок на изображения из документации (`image_path.py`)

Извлечение всех изображений из документации (`get_images.py`).

Далее изображения обрабатываются OCR через TesseractOCR.

Формирование Markdown из HTML страниц документации (`htmltomd.py`).

В результате получается несколько csv файлов с информацией из документации и ее изображений.

## Запуск

Установить зависимости:

> Прописать путь до `whl` для Tesseract в `requirements.txt`.

```bash
python -m venv env
env/bin/activate # Linux
env\Scripts\activate # Win
pip install -r requirements.txt
```

Запуск скриптов в порядке из описания.
