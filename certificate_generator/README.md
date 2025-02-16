Certificate Generator

A simple web-based Certificate Generator that allows users to upload an Excel file and generate certificates.

Features

Clean and modern UI with a beautiful background.

Upload Excel file for certificate generation.

Fully responsive design.

Easy to use.

Prerequisites

Ensure you have the following dependencies installed:

Python 3.x

Flask (pip install flask)

OpenCV (pip install opencv-python)

Pandas (pip install pandas)

ReportLab (pip install reportlab)

Installation

Clone this repository:

git clone https://github.com/yourusername/certificate-generator.git

Navigate to the project directory and install dependencies:

cd certificate-generator
pip install -r requirements.txt

Run the Flask server:

python app.py

Open your browser and go to:

http://127.0.0.1:5000

File Structure

certificate-generator/
│── certificate-app/
│   ├── templates/
│   │   ├── index.html  # HTML file for the UI
│   ├── app.py  # Flask backend
│── requirements.txt  # Dependencies list
│── README.md  # Documentation

Usage

Upload an Excel file with the required details.

Click "Generate Certificates."

Download the generated certificates.

License

This project is open-source under the MIT License.
