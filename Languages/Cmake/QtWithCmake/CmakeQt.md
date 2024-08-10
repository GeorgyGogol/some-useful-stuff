* [Назад](../Readme.md)

- [Qt с CMake](#qt-с-cmake)
  - [Поиск и включение](#поиск-и-включение)
  - [Включение автогенерации](#включение-автогенерации)
  - [Автогенерация](#автогенерация)
  - [Подключение](#подключение)
- [Финал](#финал)

# Qt с CMake

Подключение Qt библиотеки с помощью Cmake

Т.к. я использую Qt 6, то примеры актуальны для Qt6.x.x; для младших версий меняется цифра (6 -> 5 или 4, ниже 4 вроде как нет поддержки)

## Поиск и включение

```cmake
find_package(Qt6 6.8 REQUIRED COMPONENTS Core Widgets gui)
qt_standard_project_setup()
```

## Включение автогенерации

```cmake
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
```

Так же, чтобы сгенерированные файлы были видны для проекта, нужно включить директорию для включения

```cmake
set(CMAKE_INCLUDE_CURRENT_DIR ON)
```

Через отдельный путь пока не нашел

## Автогенерация

```cmake
qt6_wrap_ui(
   PR_UI_HEADERS
   sources/MWindow.ui
)
```

Таким же образом оборачиваются cpp и h файлы (qt6_wrap_cpp, qt6_wrap_h).

## Подключение

target_link_libraries(SomeExe PRIVATE Qt6::Core Qt6::Widgets Qt6::Gui)

# Финал

Все, вы великолепны)))

