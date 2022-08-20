from pathlib import Path


def remove_comments(line: str) -> str:
    array = line.split("#")
    if len(array) > 1:
        array.pop()
    return array[0]


def load_settings(file_name: str) -> dict[str, str]:
    settings = {}
    file_path = (Path('.') / file_name)
    with file_path.open(mode='r') as file:
        for line in file.readlines():
            line = remove_comments(line)
            items = line.replace('\n', '').split("=")
            if len(items) > 1:
                key = items.pop(0).strip()
                settings[key] = '='.join(items).strip()
    return settings
