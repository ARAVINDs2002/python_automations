import os
import zipfile
from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import black
from PIL import Image
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Paths
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "certificates"
TEMPLATE_IMAGE = "c1.png"  # Your certificate background image

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Register fonts
pdfmetrics.registerFont(TTFont("ElegantFont", "times.ttf"))
pdfmetrics.registerFont(TTFont("Verdana", "verdana.ttf"))

def create_certificate(name, rank, output_path):
    """Generates a certificate PDF for a given name and rank."""
    img = Image.open(TEMPLATE_IMAGE)
    width, height = img.size

    c = canvas.Canvas(output_path, pagesize=(width, height))
    c.drawImage(TEMPLATE_IMAGE, 0, 0, width, height)

    text_x = width / 2
    text_y = height / 2 + 120

    # Certificate text
    c.setFont("Verdana", 38)
    c.setFillColor(black)
    c.drawCentredString(text_x, text_y, "This certificate is proudly awarded to")

    # Name
    c.setFont("ElegantFont", 70)
    c.drawCentredString(text_x, text_y - 90, f"Miss/Mr {name}")

    # Achievement message
    c.setFont("Verdana", 37)
    c.drawCentredString(text_x, text_y - 180, "for outstanding academic performance")

    # Rank
    c.setFont("ElegantFont", 70)
    c.drawCentredString(text_x, text_y - 280, f"Rank: {rank}")

    c.setFont("Verdana", 37)
    c.drawCentredString(text_x, text_y - 350, "Congratulations!")

    c.save()

@app.route("/", methods=["GET", "POST"])
def index():
    """Homepage with file upload form."""
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400

        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400

        # Save uploaded file
        filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(filepath)

        # Read Excel file
        df = pd.read_excel(filepath)

        # Generate certificates
        pdf_files = []
        for _, row in df.iterrows():
            name = str(row.get("Name", "Unknown")).strip()
            rank = str(row.get("Rank", "Not Specified")).strip()
            output_pdf = os.path.join(OUTPUT_FOLDER, f"certificate_{name.replace(' ', '_')}.pdf")
            create_certificate(name, rank, output_pdf)
            pdf_files.append(output_pdf)

        # Create a ZIP file with all PDFs
        zip_path = os.path.join(OUTPUT_FOLDER, "certificates.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for pdf in pdf_files:
                zipf.write(pdf, os.path.basename(pdf))

        return send_file(zip_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
