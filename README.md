# 🎂 Employee birthdays service

---

The service parses birthdays of employees from the Dodo IS office manager's account and sends them to:

- The Telegram channel GoretskyBand
- The task queue of the "notifications-router" service.

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
