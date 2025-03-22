from flask import Flask, request, jsonify
from PIL import Image
import requests
import io

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_image():
    data = request.get_json()
    image_url = data.get("image_url")

    if not image_url:
        return jsonify({"error": "No image provided"}), 400

    response = requests.get(image_url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to download image"}), 400

    image = Image.open(io.BytesIO(response.content)).convert("RGB")

    MAX_SIZE = 150
    image.thumbnail((MAX_SIZE, MAX_SIZE))

    pixels = image.load()
    width, height = image.size
    pixel_data = [[list(pixels[x, y]) for x in range(width)] for y in range(height)]

    return jsonify({
        "width": width,
        "height": height,
        "pixeldata": pixel_data
    })

app.run(host="0.0.0.0", port=5000)
