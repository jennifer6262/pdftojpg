from flask import Flask, render_template, request, send_file
import os
import fitz  # PyMuPDF
import zipfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert_pdf_to_jpg():
    if "pdf" not in request.files:
        return "No file part", 400

    pdf_file = request.files["pdf"]
    if pdf_file.filename == "":
        return "No selected file", 400

    filename = secure_filename(pdf_file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    pdf_file.save(input_path)

    # PDF → JPG 변환
    doc = fitz.open(input_path)
    image_paths = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150)
        img_path = os.path.join(OUTPUT_FOLDER, f"page_{page_num + 1}.jpg")
        pix.save(img_path)
        image_paths.append(img_path)

    # ZIP 압축
    zip_path = os.path.join(OUTPUT_FOLDER, "converted.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for img_path in image_paths:
            zipf.write(img_path, os.path.basename(img_path))

    return send_file(zip_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
