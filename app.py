import json
from flask import Flask, render_template, request, redirect, url_for
from logging_config import setup_logging
from pathlib import Path
from PIL import Image

app = Flask(__name__)

logging_path = "logging/app.log"
contact_path = "static/configs/contact.json"
image_folder = "static/images"
allowed_extensions = {"png", "jpeg", "jpg"}
app.config["image_folder"] = image_folder


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def create_empty_png(path, width=600, height=600):
    empty_image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    empty_image.save(path)
    log.info(f"Created an empty PNG file at {path}")


def validate_paths(list_of_paths):
    if isinstance(list_of_paths, str):
        list_of_paths = [list_of_paths]

    for path_string in list_of_paths:
        path = Path(path_string)
        if path.suffix == "":
            path.mkdir(parents=True, exist_ok=True)
            continue

        path.parent.mkdir(parents=True, exist_ok=True)
        if path.name == "contact.json" and not path.exists():
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
            with path.open("w", encoding="utf-8") as f:
                json.dump(content, f, indent=4)
        elif (path.name in ["icon.png", "favicon.png"]) and not path.exists():
            create_empty_png(path=path)
        elif not path.exists():
            path.touch()


validate_paths([contact_path, image_folder, logging_path])

log = setup_logging(log_file=logging_path)


def generate_vcard(contact):
    vcard = (
        f"BEGIN:VCARD\r\n"
        f'VERSION:{contact["version"]}\r\n'
        f'N:{contact["last_name"]};{contact["first_name"]}\r\n'
        f'FN:{contact["full_name"]}\r\n'
        f'ORG:{contact["organization"]}\r\n'
        f'ADR:;;{contact["address"]};{contact["city"]};{contact["state"]};;\r\n'
        f'TEL;WORK;VOICE:{contact["work_phone"]}\r\n'
        f'TEL;CELL:{contact["cell_phone"]}\r\n'
        f'TEL;FAX:{contact["fax"]}\r\n'
        f'EMAIL;WORK;INTERNET:{contact["email"]}\r\n'
        f'NOTE:{contact["note"]}\r\n'
        f'URL:{contact["url"]}\r\n'
        f"END:VCARD"
    )

    log.debug(f"Generated vCard for {contact.get('full_name', 'unknown')}")
    return vcard


@app.route("/")
def index():
    try:
        with open(contact_path) as f:
            contact = json.load(f)
            log.info("Contact information loaded successfully")
    except FileNotFoundError as e:
        log.error(f"Contact file not found: {e}")
        contact = {}
    except json.JSONDecodeError as e:
        log.error(f"Error decoding contact file: {e}")
        contact = {}

    vcard = generate_vcard(contact)
    return render_template(
        "index.html", vcard=vcard, business_name=contact.get("label", "")
    )


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        try:
            contact = {
                "version": request.form["version"],
                "label": request.form["label"],
                "last_name": request.form["last_name"],
                "first_name": request.form["first_name"],
                "full_name": request.form["full_name"],
                "organization": request.form["organization"],
                "address": request.form["address"],
                "city": request.form["city"],
                "state": request.form["state"],
                "work_phone": request.form["work_phone"],
                "cell_phone": request.form["cell_phone"],
                "fax": request.form["fax"],
                "email": request.form["email"],
                "note": request.form["note"],
                "url": request.form["url"],
            }

            with open(contact_path, "w") as file:
                json.dump(contact, file, indent=4)
            log.info("Contact information updated successfully")
        except Exception as e:
            log.error(f"Failed to update contact information: {e}")
        return redirect(url_for("index"))

    try:
        with open(contact_path) as file:
            contact = json.load(file)
        log.info("Loaded contact information for editing")
    except FileNotFoundError as e:
        log.error(f"Contact file not found during edit: {e}")
        contact = {}
    except json.JSONDecodeError as e:
        log.error(f"Error decoding contact file during edit: {e}")
        contact = {}

    return render_template("edit.html", contact=contact)


@app.route("/edit-icon", methods=["GET", "POST"])
def edit_icon():
    if request.method == "POST":
        if "file" not in request.files or request.files["file"].filename == "":
            log.warning("No file selected for upload")
            return redirect(url_for("index"))
        file = request.files["file"]
        if file and allowed_file(file.filename):
            file.save(Path(app.config["image_folder"]) / "icon.png")
            return redirect(url_for("index"))
    return render_template("upload.html")


if __name__ == "__main__":
    log.info("Starting the Flask application")
    app.run()
