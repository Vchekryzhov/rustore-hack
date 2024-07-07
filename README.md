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

## Основные пути
- [Админка](https://rustore-api.kovalev.team/admin)
- [Поиск по корпусу статей](https://rustore-api.kovalev.team/articles)
- [Загрузка статей](https://rustore-api.kovalev.team/articles/new)

## чатбот

