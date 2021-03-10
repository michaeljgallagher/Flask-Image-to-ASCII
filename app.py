import os
from flask import Flask, flash, request, redirect, render_template
from flask.helpers import send_file
from werkzeug.utils import secure_filename
from ascii import *
import io

UPLOAD_FOLDER = "static"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "development_key")


def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def upload_form():
    return render_template("upload.html")


@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return generate_ascii(filename)


def generate_ascii(filename):
    # Generate the ASCII art
    with Image.open("static/" + filename) as img:
        resize_image(img, 150)
        img = img.convert(mode="L")
        matrix = convert_to_ascii_matrix(img, PALETTE_SHORT)
    out = convert_to_string_array(matrix)

    # Store output in memory
    return_data = io.BytesIO(out.encode("ASCII"))
    return_data.seek(0)

    # Remove uploaded file
    os.remove("static/" + filename)

    return send_file(return_data, mimetype="text/plain",
                     attachment_filename="generated_ascii.txt")


if __name__ == "__main__":
    app.run()
