from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
from pathlib import Path

app = Flask(__name__)

contact_path = "static/configs/contact.json"
image_folder = "static/images"
allowed_extensions = {"png", "jpeg", "jpg"}
app.config["image_folder"] = image_folder


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def validate_paths(list_of_paths):
    if isinstance(list_of_paths, str):
        list_of_paths = [list_of_paths]

    for path_string in list_of_paths:
        path = Path(path_string)
        if path.suffix == "":
            path.mkdir(parents=True, exist_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.name == "contact.json" and not path.exists():
                content = {
                    "version": "",
                    "last_name": "",
                    "first_name": "",
                    "full_name": "",
                    "organization": "",
                    "address": "",
                    "city": "",
                    "state": "",
                    "work_phone": "",
                    "cell_phone": "(",
                    "fax": "",
                    "email": "",
                    "note": "",
                    "url": "",
                }
                with path.open("w", encoding="utf-8") as f:
                    json.dump(content, f, indent=4)
            elif not path.exists():
                path.touch()


validate_paths([contact_path, image_folder])


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
    return vcard


@app.route("/")
def index():
    with open(contact_path) as f:
        contact = json.load(f)

    vcard = generate_vcard(contact)
    return render_template(
        "index.html", vcard=vcard, business_name="Swirless Car\nDetailing Business"
    )


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        contact = {
            "version": request.form["version"],
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

        with open(contact_path, "w") as f:
            json.dump(contact, f, indent=4)

        return redirect(url_for("index"))

    with open(contact_path) as f:
        contact = json.load(f)

    return render_template("edit.html", contact=contact)


@app.route("/edit-icon", methods=["GET", "POST"])
def edit_icon():
    if request.method == "POST":
        if "file" not in request.files or request.files["file"].filename == "":
            return redirect(url_for("index"))
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(Path(app.config["image_folder"]) / "icon.png")
            return redirect(url_for("index"))
    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
