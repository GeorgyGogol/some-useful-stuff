# Организация CMake

Два варианта, второй более корректный

```
projectDir
|---CMakeLists.txt
|---include
|---sources
|---tests
|---out || build
|---modules
|---resources
```

```
projectDir
|---CMakeLists.txt
|---Project1
|   |---include
|   |---sources
|   |---tests
|   |---resources
|---Project2
|   |---include
|   |---sources
|   |---tests
|   |---resources
|---modules
|---out || build
```

