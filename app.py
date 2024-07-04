from flask import Flask, request, jsonify, send_from_directory
import os
import cv2
import numpy as np
from sklearn.cluster import KMeans

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_dominant_colors(image_path, num_colors=5):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = img.reshape(-1, 3)
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    dominant_colors = kmeans.cluster_centers_.astype(int)
    return dominant_colors

def classify_color(color):
    r, g, b = color
    if 0 <= r <= 180 and 0 <= g <= 175 and 27 <= b <= 200:
        season_type = "Winter"
    elif 50 <= r <= 255 and 50 <= g <= 255 and 46 <= b <= 235:
        season_type = "Spring"
    elif 10 >= r >= 224 and 10 >= g >= 200 and 0 >= b >= 185:
        season_type = "Autumn"
    elif 0 <= r <= 255 and 0 <= g <= 237 and 0 <= b <= 255:
        season_type = "Summer"
    else:
        season_type = "Neutral"

    saturation = (np.max(color) - np.min(color)) / 255.0
    if saturation > 0.5:
        saturation_level = "Saturated"
    else:
        saturation_level = "Desaturated"

    if 180 <= r <= 225 and 0 <= g <= 175 and 50 <= b <= 150:
        temperature = "Warm"
    elif 50 <= r <= 184 and 60 <= g <= 250 and 100 <= b <= 120:
        temperature = "Cool"
    else:
        temperature = "Neutral"

    return season_type, saturation_level, temperature

def color_analysis(image_path):
    dominant_colors = extract_dominant_colors(image_path)
    classifications = []
    for color in dominant_colors:
        season_type, saturation_level, temperature = classify_color(color)
        classifications.append({
            'color': color.tolist(),
            'season_type': season_type,
            'saturation_level': saturation_level,
            'temperature': temperature
        })
    return classifications

def generate_complementary_palette(classifications):
    complementary_palette = []
    for classification in classifications:
        color = classification['color']
        season_type = classification['season_type']
        saturation_level = classification['saturation_level']
        temperature = classification['temperature']

        if season_type == "Winter":
            complementary_color = [255 - color[0], 255 - color[1], 255 - color[2]]
        elif season_type == "Spring":
            complementary_color = [255 - color[0], color[1], color[2]]
        elif season_type == "Autumn":
            complementary_color = [color[0], 255 - color[1], 255 - color[2]]
        elif season_type == "Summer":
            complementary_color = [color[0], color[1], 255 - color[2]]

        if saturation_level == "Desaturated":
            complementary_color = [int(c * 0.75) for c in complementary_color]
        if temperature == "Warm":
            complementary_color[0] = min(255, complementary_color[0] + 50)
            complementary_color[2] = min(255, complementary_color[2] + 50)
        elif temperature == "Cool":
            complementary_color[1] = min(255, complementary_color[1] + 50)
            complementary_color[2] = min(255, complementary_color[2] + 50)

        complementary_palette.append(complementary_color)
    return complementary_palette

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        classifications = color_analysis(filepath)
        complementary_palette = generate_complementary_palette(classifications)
        result = {
            'classifications': classifications,
            'complementary_palette': complementary_palette
        }
        return jsonify(result)

@app.route('/', methods=['GET'])
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
