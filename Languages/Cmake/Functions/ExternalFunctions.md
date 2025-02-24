* [Назад](../Readme.md)

- [Дополнительные приколдесы](#дополнительные-приколдесы)
  - [enable\_testing()](#enable_testing)
  - [Generating export header](#generating-export-header)
  - [Package Config Helpers](#package-config-helpers)

# Дополнительные приколдесы

В этом разделе подробно рассмотрим заклинания, описывающие поведение сборки.

## enable_testing()

Команда, включающая тестирование.

Собранный проект юнит-тестирования помещается в директорию testing

## Generating export header

**GenerateExportHeader**

Приколдес, актуальный для библиотек динамической линковки. Создает заголовочный файл, в котором определяется макрос импорта-экспорта:

```cmake
include(GenerateExportHeader)
generate_export_header(Project)
target_include_directories(Project PUBLIC ${CMAKE_CURRENT_BINARY_DIR})
```

Эта часть абстрактного скрипта проекта Project создает заголовочный файл Project_export.h (в директории с кэшем) и включает директорию с генерированным файлом в проект с публичным уровнем доступа, который позволит увидеть оный внешним проектам. В самом проекте макрос для экспорта будет называться "PROJECT_EXPORT".

Более продвинутое (и тонкое) использование:

```cmake
set(PROJECT_EXPORT_MACRO PROJECT_EXPORT)
set(PROJECT_EXPORT_PATH ${PROJECT_DIR}/include/Project/generated)
set(PROJECT_EXPORT_FILE ${PROJECT_EXPORT_PATH}/project_export.h)

include(GenerateExportHeader)
generate_export_header(
    Project
    EXPORT_MACRO_NAME ${PROJECT_EXPORT_MACRO}
    EXPORT_FILE_NAME  ${PROJECT_EXPORT_FILE}
)

tartget_sources(Project PRIVATE ${PROJECT_EXPORT_FILE})
target_include_directories(Project PUBLIC ${PROJECT_EXPORT_PATH})
```

Позволяет явно задать и название макроса экспорта, и файл для включения, и подключить именно нужный файл, и включить именно ту директорию, в которую будет сгенерирован файл. 

## Package Config Helpers

**CMakePackageConfigHelpers**

Пакет, облегчяющий жизнь создателям модулей. По шаблону, задаваемому тобой, генерирует красивый файл для настройки модуля.

