from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

def generate_vcard(contact):
    vcard = (
        f'BEGIN:VCARD\r\n'
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
        f'END:VCARD'
    )
    return vcard

@app.route('/')
def index():
    with open('contact.json') as f:
        contact = json.load(f)

    vcard = generate_vcard(contact)
    return render_template('index.html', vcard=vcard, business_name="Swirless Car\nDetailing Business")

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        contact = {
            "version": request.form['version'],
            "last_name": request.form['last_name'],
            "first_name": request.form['first_name'],
            "full_name": request.form['full_name'],
            "organization": request.form['organization'],
            "address": request.form['address'],
            "city": request.form['city'],
            "state": request.form['state'],
            "work_phone": request.form['work_phone'],
            "cell_phone": request.form['cell_phone'],
            "fax": request.form['fax'],
            "email": request.form['email'],
            "note": request.form['note'],
            "url": request.form['url']
        }

        with open('contact.json', 'w') as f:
            json.dump(contact, f, indent=4)
        
        return redirect(url_for('index'))

    with open('contact.json') as f:
        contact = json.load(f)
    
    return render_template('edit.html', contact=contact)

if __name__ == '__main__':
    app.run(debug=True)