from flask import Flask, render_template, request, url_for, send_file
import pandas as pd
import compute

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    # Assuming the file is a CSV file, you can modify it based on your needs
    df = pd.read_excel(file)
    try:
        result = compute.calculate(df)
        return result
    except:
        return 'Error: Please use the file format specified in the instructions'

if __name__ == '__main__':
    app.run(debug=False)

