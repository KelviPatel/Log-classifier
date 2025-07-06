from flask import Flask, request, send_file, render_template
import pandas as pd
import os
from classify import classify

app = Flask(__name__)

UPLOAD_FOLDER = 'Data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('logs.html') 

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in request", 400
    
    file = request.files['file']
    
    if file.filename == '':
        return "No file selected", 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    df = pd.read_csv(filepath)
    logs = list(zip(df['source'], df['log_message']))
    df['target'] = classify(logs)

    output_path = os.path.join(UPLOAD_FOLDER, 'output.csv')
    df.to_csv(output_path, index=False)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
