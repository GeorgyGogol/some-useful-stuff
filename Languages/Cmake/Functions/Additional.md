* [Назад](../Readme.md)

- [Additional Spells](#additional-spells)
  - [configure\_file](#configure_file)
  - [file](#file)
  - [foreach](#foreach)
  - [list](#list)
  - [message](#message)
  - [option()](#option)
  - [target\_compile\_definitions](#target_compile_definitions)

# Additional Spells

В этой части будут дополнительные приблуды, которые не прям обязательны для использования

## configure_file

Конфигурирование файла для проекта по заданному шаблону

Синтаксис-копипаста:

```CMake
configure_file(
    inputFile.ext.in
    output_inputFile.ext
)
```

* inputFile.ext.in - название и относительный путь к файлу-шаблону
* output_inputFile.ext - название и относительный путь к настроенному файлу
* ext - разрешение файла, в целом может быть любым

Чтобы выполнить копирование (и только копирование), без изменений, можно добавить в конец волшебное слово "COPYONLY".
В таком случае, будет выполнено копирование файла без внутренних изменений.

А как сделать этот файл шаблона? Как CMake поймет, что и как делать?

Создание файла-шаблона достаточно простое:

```cpp
#cmakedefine Var_bool
#cmakedefine Var_String @VAR_STRING@
```

```cpp
#define Var_bool
#define Var_String "String contains"
// Or
/* #undef Var_bool */
```

При этом в проекте творится примерно такое:

```CMake
option(Var_bool OFF)
set(Var_String "String contains")

configure_file(
    TestFile.h.in
    include/TestFile.h
)
```

Таким образом, настройки из CMakeLists перекочевывают в настроенный файл.

Документация: https://cmake.org/cmake/help/latest/command/configure_file.html

## file

Синтаксис-копипаста в ключе С++:

```cmake
file(GLOB SomeFiles src/*.cpp)
```

Заклинание, которое собирает файлы по маске.

## foreach

Команда для перебора списка.

Синтаксис-копипаста:

```CMake
foreach(each ${LIST_VAR})
    # some staff
endforach()
```

Полезно, если нужно перебрать список и на основе каждого элемента списка сделать что-то.

## list

Метод взаимодействия со списками.

Синтаксис-копипаста:

```CMake
list(APPEND SOME_LIST_2 SOME_VALUE)
```

```CMake
list(TRANSFORM SOME_LIST PREPEND SOME_STRING_VALUE)
```

* APPEND - Дополнить список значением (в конец)
* TRANSFORM - Изменить содержимое списка следующим образом:
    * PREPEND - Добавлением в начало каждого элемента значения


## message

Выводит сообщение в **консоли сборки**.

```cmake
message("<text>")
message(<tag> "<text>")
message(<tag> "<some message>: ${SOME_VARIABLE}")
```

* tag - Тип сообщения, вроде как не обязательный, но без него не работает
* text - Текст сообщения

Бывали случаи, когда первый вариант не работал. **Лучше всего** пользоваться тегами. Так правильно и сообщения выводятся в соответствующем тегу формате.

Тэги:

* STATUS - обычное сообщение, выводит информацию
* WARNING - предупредительное сообщение, немного выделяется на фоне логов
* DEBUG - дебажное сообщение
* FATAL_ERROR - фатальная ошибка, после чего останавливается обработка и генерация

## option()

Создание флага опции сборки. Добавляет какое-то значение - настройку - определяемую извне. Например: нужно ли собирать юниттесты, активировать какие-то дополнительные участки кода, название пространства имен и все в таком духе.

Обычный "option" задает только флаг. Для создания опций другого вида (строки, перечисления) придется пойти на хитрость и использовать set.

Синтаксис-копипаста:

```cmake
option(OptionName "Description" OFF)
set(OptionName2 "Default value (string)" CACHE STRING "Description")
```

Это определение опции сборки.

В [примере выше](#New%20project%20Base) задается опция сборки ProjectName_LIB для определения во что собирать проект - в исполняемый файл (для OFF) или динамическую библиотеку (для ON). По-умолчанию (если не определить ON/OFF) будет являться OFF.

Задается до выполнения конфигурации в GUI симейка или во время конфигурации командой:

```sh
cmake -D DProjectName_LIB=ON
```

(В команде не уверен)

Как видно, синтаксис примерно такой: "-D< optionName >=ON/OFF"

## target_compile_definitions

Добавление дополнительных определений компилятору

Синтаксис-копипаста:

```CMake
target_compile_definitions(<target> PRIVATE Definition)
```

* target - Оригинальное название компилируемой единицы, использование алиаса не допускается
* PRIVATE - Модификатор видимости (может быть INTERFACE|PUBLIC|PRIVATE)
* Definition - дополнительное определение, можно в кавычках; может иметь значение (через равно)

Нюансы и более полное описание команды можно посмотреть [тут](https://cmake.org/cmake/help/latest/command/target_compile_definitions.html).


