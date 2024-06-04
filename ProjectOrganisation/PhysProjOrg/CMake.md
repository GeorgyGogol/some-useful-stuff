* [Назад](Readme.md)

- [Организация CMake](#организация-cmake)
- [Проект-монолит](#проект-монолит)
- [Модульный проект](#модульный-проект)

# Организация CMake

Про сам синтаксис можно посмотреть [тут](../../Languages/CMake.md)

Здесь же про то, как физически может быть организован проект. На текущий момент выработал два варианта. На мой взгляд второй более корректный и гибкий, первый - более быстрый.

Отправной точкой служит projectDir - корневая директория (репозитория) проекта. В этой директории предлагаю следующие поддиректории:

* include - для включения во внешних проектах
* sources - исходный код проекта ("закрытый" для внешних проектов)
* tests - юнит-тесты и все с этим связанное
* modules - для внешних проектов
* resources - для ресурсов проекта
* out или build - директория для работы Cmake

# Проект-монолит

Но на самом деле, как не хотелось бы монолита, у него выделяется проект для тестирования

```
projectDir
|---CMakeLists.txt
|---include/projectDir
|---sources
|---tests
|---out || build
|---modules
|   |---Module1
|
|---resources
|---doc
```

# Модульный проект

```
projectDir
|---CMakeLists.txt
|---out || build
|---doc
|---Project1
|   |---CMakeLists.txt
|   |---include/Project1
|   |---sources
|   |---tests
|   |---resources
|
|---Project2
|   |---CMakeLists.txt
|   |---include/Project2
|   |---sources
|   |---tests
|   |---resources
|
|---modules
    |---Module1
    |   |---...
    |
    |---Module2
        |---CMakeLists.txt
        |---include/Module2
        |---sources
        |---tests
        |---resources
```

Нет полной уверенности

