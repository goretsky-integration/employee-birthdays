def clean_employee_full_name(name: str) -> str:
    prefixes_to_clean = (
        'СЗ',
        'У',
        'К',
    )
    for prefix in prefixes_to_clean:
        name = name.removeprefix(f'{prefix} ').strip()
    return name
