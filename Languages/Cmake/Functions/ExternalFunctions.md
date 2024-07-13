* [Назад](../Readme.md)

- [Дополнительные приколдесы](#дополнительные-приколдесы)
  - [enable\_testing()](#enable_testing)
  - [Generating export header](#generating-export-header)

# Дополнительные приколдесы

В этом разделе подробно рассмотрим заклинания, описывающие поведение сборки.

## enable_testing()

Команда, включающая тестирование.

Собранный проект юнит-тестирования помещается в директорию testing

## Generating export header

**GenerateExportHeader**

Приколдес, актуальный для библиотек динамической линковки. Создает заголовочный файл, в котором определеяется макрос импорта-экспорта:

```cmake
include(GenerateExportHeader)
generate_export_header(Project)
target_include_directories(Project PUBLIC ${CMAKE_CURRENT_BINARY_DIR})
```

Эта часть абстрактного скрипта проекта Project создает заголовочный файл Project_export.h (в
директории с кэшем) и включает директорию с генерированным файлом в проект с публичным уровнем доступа, который позволит увидеть оный внешним проектам

