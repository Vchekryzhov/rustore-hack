# Rustore Помощник 

## Запуск
```bash
docker-compose down && docker-compose up --build
```

## Подготовка Данных
1. запустите приложение командой выше и откройте [localhost:3035/articles/new]()
2. Загрузите в форму файл с статьями который лежит в репо  public/articles.csv
2. Откройте админку и можете видеть что создаются статьи http://localhost:3035/admin/article
3. Проверте что работает базовый RAG http://localhost:3035/articles

## Прозрачность данных
В файле app/jobs/llm_job.rb находится job который подготваливает ответ для пользователя.

В файле models/llm происходит запрос на LLM

В файле models/semantic_search.rb происходит поиск контекста в базе данных

На странице https://rustore-api.kovalev.team/admin/message можно видеть список всех сообщенией 
в системе и если зайти в какое нибудь сообщение можно увидеть контекст который был отправлен в LLM и референсы на статьи из которых взят контекст
## Основные пути
- [Чатбот](https://rustore.kovalev.team) можно зайти под гостем или под админом `manager:zak2`
- [Админка](https://rustore-api.kovalev.team/admin)
- [Поиск по корпусу статей](https://rustore-api.kovalev.team/articles)
- [Загрузка статей](https://rustore-api.kovalev.team/articles/new)

------
## LLM
Находится в папке LLM в корне репозитория

Нужно добавить свой ключ ngrok, для проксирования

файл  LLM/hf.py содержит код запуска инференса LLM через huggingface

файл  LLM/vllm.py содержит код запуска инференса VLLM,которая ускоряет инференс в 3 раза

Используем модель Phi-3-medium-128k-instruct, лицензия MIT(можно использовать в любых целях)

Можно в целом поменять модель с Phi-3 и все заведется

-----
## Парсинг документации


# Docs parser 
Находится в папке docs_parser корне репозитория

Парсер документации [RuStore](https://www.rustore.ru/help/).

## Как работает

Берет все страницы из `sitemap.xml` и собирает (`main.py`).

На момент хакатона `Количество страниц документации: 479`.

Извлечение уникальных ссылок на изображения из документации (`image_path.py`)

Извлечение всех изображений из документации (`get_images.py`).

Далее изображения обрабатываются OCR через TesseractOCR.

Формирование Markdown из HTML страниц документации (`htmltomd.py`).

В результате получается несколько csv файлов с информацией из документации и ее изображений.

## Запуск парсера

Установить зависимости:

> Прописать путь до `whl` для Tesseract в `requirements.txt`.

```bash
python -m venv env
env/bin/activate # Linux
env\Scripts\activate # Win
pip install -r requirements.txt
```

Запуск скриптов в порядке из описания.
-------

