# 🎂 Employee birthdays service

[![Pytest](https://github.com/goretsky-integration/employee-birthdays/actions/workflows/pytest.yml/badge.svg)](https://github.com/goretsky-integration/employee-birthdays/actions/workflows/pytest.yml)
[![Pylint](https://github.com/goretsky-integration/employee-birthdays/actions/workflows/pylint.yml/badge.svg)](https://github.com/goretsky-integration/employee-birthdays/actions/workflows/pylint.yml)
[![Mypy](https://github.com/goretsky-integration/employee-birthdays/actions/workflows/mypy.yml/badge.svg)](https://github.com/goretsky-integration/employee-birthdays/actions/workflows/mypy.yml)

---

The service parses birthdays of employees from the Dodo IS office manager's account and sends them to the Telegram channel GoretskyBand.

## Installation

1. Clone this repository
    ```git
    git clone https://github.com/goretsky-integration/employee-birthdays
    ```

2. Create virtual environment
    ```bash
    poetry env use python3.11
    ```

3. Activate it
    ```bash
    poetry shell
    ```

4. Install dependencies
    ```bash
    poetry install --without dev
    ```

5. Copy config and setup it
    ```bash
    cp config.example.toml config.toml
    ```

6. Run the service
    ```bash
    python3.11 src/main.py
    ```
