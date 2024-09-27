## Developers Guide

### 1. Naming Conventions
This project contains modules from multiple subprojects. When working with any of these submodules please follow the naming conventions outlined here. 

#### 1.1. Python
For python programs use the following convention consistant with [PEP 8](https://peps.python.org/pep-0008/#class-names) and [PEP 257](https://peps.python.org/pep-0257/) style guides.


1. **Enums:** `UPPERCASE` (e.g., `DOSTUFF`)
2. **Globals:** `UPPER_SNAKE_CASE` (e.g., `GLOBAL_REGISTRY`)
3. **Constants:** `UPPER_SNAKE_CASE` (e.g., `GLOBAL_REGISTRY`)
4. **Variables:** `snake_case` (e.g., `max_value`)
5. **Functions:** `snake_case` (e.g., `do_stuff`)
6. **Methods:** `snake_case` (e.g., `do_stuff`)
   
***Note***

This is a pyqt project where the typical convention is for methods to be labelled with lowerUpper case for historic reasons. Hence, an exception exists for methods of QWidget inheriting classes.

7. **Classes:** `PascalCase` (, e.g., `DoStuff`)
8. **Modules and Packages:** `lowercase` (e.g., `mymodule`)
9.  **File Names:** `snake_case` (e.g., `my_file.py`)

All classes, functions and methods should be documented with PEP257 docstrings and read_the_files. 