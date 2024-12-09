* [Назад](./Readme.md)

- [Install](#install)
  - [Синопсис](#синопсис)
  - [Команда Install](#команда-install)
  - [CMakePackageConfigHelpers](#cmakepackageconfighelpers)
  - [Так как же задать правила установки](#так-как-же-задать-правила-установки)
- [Соус](#соус)

# Install

В этой статье описывается, как правильно написать правила для установки пакета, чтобы все было хорошо, все работало и не было слезок и костылей.

Инсталл - такая команда, которая установит модуль и внедрит его в почти весь CMake так, что ты сможешь пользовать пакет в разработке других приложений и/или модулей.

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

## CMakePackageConfigHelpers

Специальный модуль, включаемый в базовую поставку CMake для автогенерации .cmake файлов конфигурации проекта.

По вот такому шаблону:

```CMake
@PACKAGE_INIT@

include ( "${CMAKE_CURRENT_LIST_DIR}/MyProjectTargets.cmake" )
check_required_components(MyProject)
```

Генерирует конфигурационный файл, по которому команда find_package() будет находить модуль.

## Так как же задать правила установки

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
        DESTINATION SomeLib/include
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

# Соус

* https://cmake.org/cmake/help/book/mastering-cmake/chapter/Install.html
* https://cmake.org/cmake/help/latest/guide/importing-exporting/index.html#creating-a-package-configuration-file

