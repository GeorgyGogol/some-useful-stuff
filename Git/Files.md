* [Назад](./Readme.md)

- [Файлы в репозитории](#файлы-в-репозитории)
  - [.gitignore](#gitignore)
  - [.gitkeep](#gitkeep)
  - [.gitmodules](#gitmodules)
- [Файлы в папке .git](#файлы-в-папке-git)
  - [COMMIT\_EDIT](#commit_edit)

# Файлы в репозитории

В этом разделе собрана информация по физическим файлам, используемым СКВ Git

## .gitignore

Шаблоны путей и названий, которые будут игнорироваться

## .gitkeep

Пустой файл, наличие которого гарантирует попадание директории в индекс и отслеживание

## .gitmodules

Файл с описанием подмодулей репозитория. Обычно содержит информацию о: 

1. Название
2. Нахождение в репозитории
3. URL или адрес основного репозитория
4. Ветка, используемая в текущем репозитории

# Файлы в папке .git

В целом наличие этой папки говорит о наличии репозитория в текущем месте. В ней хранятся файлы:

1. Необходимые для работы
2. Определяющие поведение (хуки)
3. Временные

## COMMIT_EDIT

Файл, создающийся во время операции commit с текстом, который будет использован в коммите

