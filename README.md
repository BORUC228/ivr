## IVR-Kit Tests
Python Version: 3.7
### Установка Python: https://python-scripts.com/install-python
Запуск тестов:
Перед запуском необходимо установить requirements.txt
```
pip install -r /path/to/requirements.txt
```
Затем для запуска:
```
pytest - запуск набора всех тестов находящихся в текущей директории
pytest <filename> - запуск тестов из файла
pytest <filename>:<defname> - запуск определённого теста из файла
```
### Examples:
```
pytest
pytest test_get_token.py
pytest test_get_token.py::test_take_token_with_valid_auth
```
