import colorgram
from flask import Flask, render_template, url_for, redirect, request, flash
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/temp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dsfewfer45efer'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_colors(file):
    rgb_colors = []
    colors = colorgram.extract(file, 20)
    for color in colors:
        r = color.rgb.r
        g = color.rgb.g
        b = color.rgb.b
        new_color = (r, g, b)
        rgb_colors.append(new_color)
    return rgb_colors


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('home'))
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('home'))
        if not allowed_file(file.filename):
            flash('The file you selected is not an image file')
            return redirect(url_for('home'))
        if file and allowed_file(file.filename):
            file_name = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            list_of_colours = extract_colors(file=f'static/temp/{file_name}')
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            return render_template('palette.html', colours=list_of_colours)
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
