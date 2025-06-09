from encodings import johab
from flask import Flask, render_template, request, jsonify
from PIL import Image
import requests
import os
from classes.RecipeGenerationPipeline import RecipeGenerationPipeline
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/generate', methods=['POST'])
def generate():
    ingredients = request.form.get('ingredients')
    cuisine_type = request.form.get('cuisine_type')
    pipline = RecipeGenerationPipeline(ingredients, cuisine_type)
    result = pipline.execute()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
