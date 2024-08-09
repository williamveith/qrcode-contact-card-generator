# Contact Badge Creator Flask Application

## Overview

This Flask application provides a streamlined web interface designed to manage and display a single contact's information in a vCard format. It allows for the creation of a personalized contact badge, which includes a QR code on the front linked to the vCard and a custom icon on the back. Ideal for individuals who need a quick, printable badge for networking or identification purposes, the application supports editing the contact details and icon through an intuitive web interface.

## Features

- **Create and Print Personalized Badges:** Users can generate and print a badge featuring a QR code derived from the contact's vCard on the front, and a custom icon on the back, with the contact's name displayed prominently on both sides.

- **Singular Contact Management:** The application is designed to handle a single set of contact details at any given time, allowing users to focus on managing and updating their own contact information efficiently.

- **Edit Contact Details:** Provides a simple form to edit or update the stored vCard information, ensuring the badge displays the most current information.

- **Upload and Customize Icon:** Users can upload or update the icon associated with the contact, which is displayed on the back of the badge for added personalization.

- **Responsive Design:** The web interface adjusts seamlessly for various devices, enhancing usability and ensuring easy access whether on a mobile phone, tablet, or desktop.

- **Interactive Navigation Bar:** Features a navigation bar that offers direct access to print the badge, edit contact details, or change the icon, simplifying the user experience and workflow.

## Application Workflow

- **Print Badge:** Users can directly print a badge that features a QR code on the front linked to the contact's vCard and a customizable icon on the back.

- **Edit Contact:** Access a streamlined form to edit or update the vCard information of the contact, which is immediately reflected in the QR code and badge display.

- **Change Icon:** Upload or change the icon that appears on the back of the badge, allowing for further customization.

This focus on managing a singular contact makes the application particularly useful for personal branding, providing a simple yet effective tool for creating a professional-looking badge.

## Project Structure

It is a basic flask app. Run app.py or use the VSCode Python Debugger: Flask launch item

    qrcode-contact-card-generator
    ├── Dockerfile
    ├── README.md
    ├── app.py
    ├── config
    │   ├── __init__.py
    │   └── configs.py
    ├── docker-compose.yml
    ├── logger
    │   ├── __init__.py
    │   └── configs.py
    ├── requirements.txt
    ├── static
    │   ├── configs
    │   ├── css
    │   │   ├── form.css
    │   │   └── general.css
    │   └── images
    │       └── favicon.png
    └── templates
        ├── edit.html
        ├── index.html
        └── upload.html
