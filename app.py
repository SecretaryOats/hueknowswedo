from flask import Flask, request, render_template, redirect, url_for
from PIL import Image
import colorsys
import os

app = Flask(__name__)

def get_triadic_colors(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    triadic_colors = []
    for i in range(3):
        triadic_h = (h + i * 1/3) % 1.0
        triadic_r, triadic_g, triadic_b = colorsys.hls_to_rgb(triadic_h, l, s)
        triadic_colors.append((int(triadic_r * 255), int(triadic_g * 255), int(triadic_b * 255)))
    return triadic_colors

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            image = Image.open(file.stream)
            # Assuming the skin color is the most frequent color in the image for simplicity
            colors = image.getcolors(image.size[0] * image.size[1])
            most_frequent_color = max(colors, key=lambda t: t[0])[1]
            triadic_colors = get_triadic_colors(*most_frequent_color)
            return render_template('index.html', triadic_colors=triadic_colors)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
