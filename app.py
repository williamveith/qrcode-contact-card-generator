import json
from flask import Flask, render_template, request, redirect, url_for
from logger import log
from config import *
from pathlib import Path

app = Flask(__name__)

allowed_extensions = {"png", "jpeg", "jpg"}
app.config["image_folder"] = IMAGE_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

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
        with open(CONTACT_PATH) as f:
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

            with open(CONTACT_PATH, "w") as file:
                json.dump(contact, file, indent=4)
            log.info("Contact information updated successfully")
        except Exception as e:
            log.error(f"Failed to update contact information: {e}")
        return redirect(url_for("index"))

    try:
        with open(CONTACT_PATH) as file:
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
    app.run(host='0.0.0.0')
