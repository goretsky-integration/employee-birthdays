def clean_employee_full_name(name: str) -> str:
    prefixes_to_clean = (
        'СЗ',
        'сз',
        'Сз',
        'сЗ',
        'У',
        'у',
        'К',
        'к',
        'k',
        'K',
    )
    for prefix in prefixes_to_clean:
        name = name.removeprefix(f'{prefix} ').strip()
    return name
