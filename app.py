import openai
import os, json
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded file
    file = request.files['file']

    # Read CSV file using Pandas
    data = pd.read_csv(file)

    # Display the first five rows of the data
    return data.head().to_html()

if __name__ == '__main__':
    app.run(debug=True)
