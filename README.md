# Lab_work_numerical_methods

Реализация методов Рунге-Кутта 2, 3, 4 порядков:

    - main.py - интерфейс программы, построение графиков
    - setup.py - скрипт компиляции си-кода, реализующего алгоритм Рунге-Кутта
    ("python setup.py build_ext --inplace" - bash скрипт, компилирующий cython код в си библиотеку)
    - output_data.json - файл с данными после реализации метода (для построения графиков)
    - requirements.txt - файл с зависимостями

    Директории:
    - FastRk - си реализация библиотеки методов Рунге-Кутта
        - cmethods.c - библиотека
        - cmethods.pyx - cython код
    - inputdata - директория с начальными условиями для каждой задачи
    - source - директория с исходным кодом
        - methods.py - класс, реализующий работу методов Рунге-Кутта
        - functions.py - исходные функции

    !Для корректной работы программы запуск скриптов!:
        - pip install -r requirements.txt
        - python3 -m venv env
        - python setup.py build_ext --inplace
