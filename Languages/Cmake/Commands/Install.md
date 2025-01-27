* [Назад](./../Readme.md)

- [Install](#install)
  - [Синопсис](#синопсис)
  - [Команда Install](#команда-install)
  - [CMakePackageConfigHelpers](#cmakepackageconfighelpers)
  - [Наглядный пример](#наглядный-пример)
  - [Объяснение магии](#объяснение-магии)
    - [target\_include\_directory](#target_include_directory)
    - [is\_proj\_top\_level](#is_proj_top_level)
  - [Возможные вопросы](#возможные-вопросы)
    - [Проверка существования](#проверка-существования)
  - [IMPORTED\_LOCATION error](#imported_location-error)
- [Соус](#соус)

# Install

В этой статье описывается, как правильно написать правила для установки пакета, чтобы все было хорошо, все работало и не было слезок и костылей.

```cmake --install``` - это такая команда, которая установит скомпилированный модуль по заданному префиксу пути установки. В зависимости от этого префикса, полученный модуль может быть использован либо локально каким-то проектом, либо глобально проектами по всему компьютеру (в зависимых модулях указать, где искать и откуда тянуть). Так что ты сможешь пользовать пакет в разработке других приложений и/или модулей.

## Синопсис

CMake предоставляет возможность производить установку пакета и использовать его различными таргетами. Подключение, как правило, происходит с помощью команды find_package().

Это позволяет единожды выполнить установку определенной версии библиотеки для использования другими проектами именно этой, установленной библиотекой. Таким образом, после установки модуль становится общим для остальных таргетов. В отличие от подхода с подпапками, когда один и тот же модуль каждый раз интегрируется в проект.

Для работы этой архимагии нужно:
1. Сам проект модуля
2. Определить внешний API
3. Обозначить скомпилированные части модуля
4. Сделать скрипты для CMake, что и где искать

Пункты достигаются следующими шагами:
1. Пишем модуль и определяем его API
2. Пишем в CMake модуля install-правила
3. Выполняем настройку и конфигурацию проекта с нужным CMAKE_INSTALL_PREFIX
4. Кастуем заклинания build для сборки бинарей и install для установки
5. ???
6. В клиентском модуле настраиваем CMAKE_PREFIX_PATH и выполняем заклинание find_package()
7. Вы великолепны

## Команда Install

Специальная команда, которая определяет поведение системы сборки при получении команды "установи".

Актуально и кратко с версии CMake 2.4 выглядит примерно следующим образом:

```CMake
install([TYPE] < WHAT > DESTINATION < WHERE > [...])
```

Таким образом, задаются правила, причем для каждой части модуля:
* TARGETS - Единицы компиляции проекта
* DIRECTORY - Директории с файлами и поддиректориями (иерархия сохраняется)
* FILES - Именно файлы, которые будут сложены в определенное место (иерархия не сохраняется)
* EXPORT - Генерирование и установка .cmake файлов, необходимых для включения в других проектах

Правильно наколдовав install можно добиться интеграции своего модуля в другие модули.

Я придерживаюсь примерно следующей последовательности:

1. install target
2. install directory (public headers)
3. configure export cmake
4. install cmake config file

## CMakePackageConfigHelpers

Специальный модуль, включаемый в базовую поставку CMake для автогенерации .cmake файлов конфигурации проекта.

По вот такому шаблону:

```CMake
@PACKAGE_INIT@

include ( "${CMAKE_CURRENT_LIST_DIR}/MyProjectTargets.cmake" )
check_required_components(MyProject)
```

Генерирует конфигурационный файл, по которому команда find_package() будет находить модуль с названием MyProject.

## Наглядный пример

В общем скрипт выглядит примерно так:

```CMake
# Контекст до начала магии
# Тут как обычно - делаем таргет, определяем исходники и пути...
add_library(SomeLib SHARED)
target_sources(SomeLib PRIVATE ${SOME_CPP_FILES} ${SOME_H_FILES})
target_include_directory(SomeLib PRIVATE ${SOME_CPP_DIRS} ${SOME_H_DIRS})

# Но для публичных путей нужно задать...
target_include_directory(
    SomeLib
    PUBLIC
    $<BUILD_INTERFACE:${SOMELIB_DIR}/include>
    $<INSTALL_INTERFACE:$<INSTALL_PREFIX>/SomeLib/include>
)

# Install rules
# Проверим, является ли проект верхнеуровневым (?)
string(COMPARE EQUAL ${CMAKE_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR} is_proj_top_level)
if(is_proj_top_level)
    # Установка юнитов компиляции
    install(
        TARGETS SomeLib
        DESTINATION SomeLib/bin
        EXPORT SomeLibTargets
    )
	
    # Установка API файлов включений
    # Либо ставим всю директорию как есть:
    install(
        DIRECTORY ${SOMELIB_DIR}/include/
        DESTINATION SomeLib
    )
    # Либо сваливаем все заголовочники в одно место:
    # install(
    #     FILES ${SOME_H_FILES}
    #     DESTINATION SomeLib/include
    # )
	
    # Генерация и установка .cmake-файлов
    install(
        EXPORT SomeLibTargets
        FILE SomeLibTargets.cmake
        DESTINATION cmake
    )
    include(CMakePackageConfigHelpers)
    configure_package_config_file(
        ${ENTRY_POINT_DIR}/cmake/Config.cmake.in
        ${ENTRY_POINT_DIR}/cmake/generated/SomeLibConfig.cmake
        INSTALL_DESTINATION cmake
    )
    install(
        FILES
        ${ENTRY_POINT_DIR}/cmake/generated/SomeLibConfig.cmake
        DESTINATION cmake
    )
endif()
```

Шаблон для генерации cmakeConfig (Config.cmake.in):

```CMake
@PACKAGE_INIT@

include ( "${CMAKE_CURRENT_LIST_DIR}/SomeLibTargets.cmake" )
check_required_components(SomeLib)
```

ВАЖНО: Не забыть в файле заменить "SomeLib" на название своего проекта. Попадался.

## Объяснение магии

### target_include_directory

Итак, у нас есть публичный апи и нам нужно указать, где его искать. Build и Install - разные команды и мы обозначаем, что использовать в том или ином случае:
* Build - определяется через BUILD_INTERFACE - ведет к директории в проекте
* Install - определяется через INSTALL_INTERFACE - ведет к директории где будут лежать файлы публичного программного интерфейса
* INSTALL_PREFIX - "плейсхолдер", обозначающий какой-либо путь к директории, куда будет выполнена установка. На сколько понял, это не позволит делать жесткие абсолютные пути

### is_proj_top_level

Проверка, является ли проект верхнеуровневым. У меня нет уверенности в необходимости этого.

Начиная с версии 3.21 введена специальная переменная: PROJECT_IS_TOP_LEVEL, которая говорит является ли проект верхнеуровневым или нет. До версии 3.21 делается следующим образом:

```cmake
string(COMPARE EQUAL ${CMAKE_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR} is_proj_top_level)
```

## Возможные вопросы

Раздел про различные ситуации, потребности и запросы.

### Проверка существования

А что, если в процессе установки, нужно проверить, существует ли файл или нет? И в зависимости от его наличия/отсутствия выполнить его установку/переустановку/ничего не делать

В таком случае пользуемся стандартной инструкцией:

```cmake
if(NOT EXISTS ${CMAKE_INSTALL_PREFIX}/${FilePath}/${FileName})
    # <...>
    install(
        FILES
        ${FileName}
        DESTINATION ${FilePath}
    )
else()
    # Anotger stuff
    # <...>
endif()
```

Где подставить на места свои значения:

* FilePath - Путь до местонахождения файла
* FileName - Название проверяемого файла

## IMPORTED_LOCATION error

В процессе выполнения команды:

```sh
cmake --install . --config Debug
```

CMake выдает ошибку про IMPORTED_LOCATION и configuration:

```txt
IMPORTED_LOCATION not set for imported target "target" configuration "Debug".
```

Связано с тем, что в процессе сборки не была использована эта конфигурация.

Решение:

1. Не использовать эту опцию при установке
2. Конфигурацию задавать на этапе сборки проекта

```sh
cmake --build . --config Debug
cmake --install .
```

# Соус

* https://cmake.org/cmake/help/book/mastering-cmake/chapter/Install.html
* https://cmake.org/cmake/help/latest/guide/importing-exporting/index.html#creating-a-package-configuration-file
* https://cmake.org/cmake/help/latest/command/install.html
* https://stackoverflow.com/questions/74587365/imported-location-not-set-for-imported-target

