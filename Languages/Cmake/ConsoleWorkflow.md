* [Назад](./Readme.md)

- [Колдовство в консоли](#колдовство-в-консоли)
  - [Конфигурирование](#конфигурирование)
  - [Сборка](#сборка)

# Колдовство в консоли

Итак, мы подготовили наш скрипт, будто это заклинание в книге. Теперь, чтобы ~~скастовать сборку~~ заставить это работать, мы должны ~~прочитать его~~ обратиться непосредственно к системе сборки CMake с просьбой сделать это.

Весь процесс делится на два этапа: конфигурирование и сборка. И два пути: GUI и консоль. Здесь - про консоль.

## Конфигурирование

Первый шаг. Суть в том, чтобы сформировать кэш CMake и подготовить оный к сборке. Шаг может быть выполнен непосредственно в директории (In-Source-Build, не рекомендуется), так и в поддиректории (Out-Source-Build, рекомендуется). Фактически, мы скармливаем системе сборки наш CMakeLists.txt, и она формирует кэш для дальнейшей сборки.

Командовать (для сборки в поддиректории build) так:

```sh
mkdir build
cd build
cmake ..
```

Таким образом, мы сформируем кэш для дельнейшего билда

## Сборка

Тут все более однозначно. В директории, в которой находится кэш, говорим:

```sh
cmake --build . --parallel
```

Это запустит сборку. Флаг parallel разрешает использовать более одного потока и выполнять сборку параллельно
