# QR Code Contact Card Generator

This was originally a 2 second project to hook up the supply store dude with a QR Code Contact Card for his business. After adding a feature that allowed the contact information to be edited, I added an icon edit feature, turning this into a general purpose app. Add your contact information and desired icon to generate a contact card with a qr code containing your VCARD & the customized icon you selected

Very very simple app that was meant to be a one off. Only pushed it to a public repo because this use case will occur again and I don't want to redo work Ive already done

## Project Structure

It is a basic flask app. Run app.py or use the VSCode Python Debugger: Flask launch item

    ```text
    qrcode-contact-card-generator
    ├── app.py
    ├── requirements.txt
    ├── static
    │   ├── configs
    │   │   └── contact.json
    │   ├── css
    │   │   ├── form.css
    │   │   └── general.css
    │   └── images
    │       ├── favicon.png
    │       └── icon.png
    └── templates
        ├── edit.html
        ├── index.html
        └── upload.html
    ```
