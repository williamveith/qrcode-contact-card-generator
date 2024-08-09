import json
from pathlib import Path
from PIL import Image
from logger import log

def create_empty_contact(path):
    content = {
        "version": "",
        "label": "",
        "last_name": "",
        "first_name": "",
        "full_name": "",
        "organization": "",
        "address": "",
        "city": "",
        "state": "",
        "work_phone": "",
        "cell_phone": "",
        "fax": "",
        "email": "",
        "note": "",
        "url": "",
    }
    with path.open("w", encoding="utf-8") as file:
        json.dump(content, file, indent=4)


def create_empty_png(path, width=600, height=600):
    empty_image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    empty_image.save(path)
    log.info(f"Created an empty PNG file at {path}")


def validate_directories(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def validate_files(path: Path):
    if path.name == "contact.json":
        create_empty_contact(path)
    elif path.name in ["icon.png", "favicon.png"]:
        create_empty_png(path=path)
    else:
        path.touch()


def validate_paths(list_of_paths):
    if isinstance(list_of_paths, str):
        list_of_paths = [list_of_paths]

    for path_string in list_of_paths:
        path = Path(path_string)
        validate_directories(path)

        if path.suffix == "":
            path.mkdir(parents=True, exist_ok=True)
        elif not path.exists():
            validate_files(path)