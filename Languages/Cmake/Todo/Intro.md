* [Назад](./Readme.md)

- [New project Base](#new-project-base)

# New project Base

[Официальный туториал](https://cmake.org/cmake/help/latest/guide/tutorial/index.html)
[Подробнее о заклинаниях](Functions/Functions.md)

Для проекта нужно всего ничего - файл CMakeLists.txt и несколько колдовских слов. При изучении очень не хватало сначала посмотреть на общую картину, так что начну с примерно общего файла. Тут я постарался нарисовать основы, которые используются для написания CMakeLists.txt

```cmake
# Блок комментариев начинается с решетки

# Объявим минимальную версию CMake
cmake_minimum_required(VERSION 3.15) # См. в подробнее

# Определяем название проекта, версию и язык соответственно
project(
    ProjectName
    VERSION 0.1.0
    LANGUAGES CXX
)
# Эти строчки устанавливают требования к используемой версии языка C++
set(CMAKE_CXX_STANDARD 26) # <- Версия С++
set(CMAKE_CXX_STANDARD_REQUIRED True) # <- Ошибка, если такой версии нет
set(CMAKE_CXX_EXTENSIONS OFF) # <- Вот в этом не разобрался и как-то не хочется

# Вот эта штучка задает настройку сборки
option(ProjectName_LIB "Buid as lib" OFF)

# Это пример и объявления переменной, и сбора исходников проекта в одно место
set(
    SOURCES
    SomeClass.h
    SomeClass.cpp
    "Utils/ISomeUtil.h"
)
# Теперь мы можем обратиться к этой вещи через ${SOURCES}

# Тоже самое, только для директорий
set(
    INCLUDE_DIRS
    Utils
)

# Пример условного оператора
if(ProjectName_LIB)
    # Это вариант для ProjectName_LIB = ON
    # Собираем библиотеку динамической компановки
    add_library(ProjectName SHARED ${SOURCES})
    # Делаем алиас на модуль
    add_library(modules::ProjectName ALIAS ProjectName)
else()
    # Собираем исполняемый exe (если для винды)
    add_executable(ProjectName STATIC main.cpp )
endif(ProjectName_LIB) # Не обязательно, можно проще: endif()

# Теперь скажем, какие директории включаются в проект
target_include_directories(ProjectName PRIVATE ${INCLUDE_DIRS})
# А вот тут, какие файлы с исходным кодом добавить
target_sources(ProjectName PRIVATE ${SOURCES})

# Добавление поддиректории
add_subdirectory(subDir)
```

