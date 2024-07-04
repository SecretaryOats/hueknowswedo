# app.py
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os
import colorsys

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def get_palette(image_path, num_colors=5):
    image = Image.open(image_path)
    image = image.convert('RGB')
    colors = image.getcolors(image.size[0] * image.size[1])
    colors.sort(key=lambda x: x[0], reverse=True)
    palette = [color[1] for color in colors[:num_colors]]
    return palette

def classify_season(color):
    r, g, b = color
    if r > g and g > b:
        return 'Autumn'
    elif g > r and r > b:
        return 'Spring'
    elif b > r and r > g:
        return 'Winter'
    else:
        return 'Summer'

def classify_warm_cool(color):
    r, g, b = color
    return 'Warm' if (r + g) > b else 'Cool'

def classify_saturation(color):
    r, g, b = color
    max_color = max(r, g, b)
    min_color = min(r, g, b)
    return 'Saturated' if (max_color - min_color) > 100 else 'Desaturated'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('image')
        palettes = []
        for file in files:
            if file:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(image_path)
                palette = get_palette(image_path)
                palettes.append(palette)
        return render_template('index.html', palettes=palettes)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
