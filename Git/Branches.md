* [Назад](./Readme.md)

# Ветки

Ветки текущего репозитория:

```
git branch
git branch qwerty - создает ветку qwerty
git branch qwerty -D - удаляет ветку qwerty
git branch -a - Ветки с удаленным репо
git branch -m oldName newName - Переименование ветки
```

# Нейминг

master
dev

Для ответвлений на ветке предлагаю использовать стиль с обратным слэшем branchName/subBranch

## Работа с внешними ссылками

```
git remote -v
git remote set-url origin --push <path>
git remote add <name> <path>
git remote remove <name>
```

1. Просмотр всех внешних связей
2. Переопределить связь, уточнить, куда делать пуш
3. Добавляет ссылку на внешнее
4. Удаляет ссылку

## Отправка ветки

Выполняется с помощью команды

```
git push <remote> <branch-name> --set-upstream
git push <remote> <tag-name>
```

