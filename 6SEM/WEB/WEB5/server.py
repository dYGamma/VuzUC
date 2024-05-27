from flask import Flask, request, render_template, send_from_directory, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_data_to_file(data):
    with open('data.txt', 'a', encoding='utf-8') as file:
        file.write(data + '\n')

@app.route('/')
def home():
    return render_template('html5_page.html')

@app.route('/index')
def index_page():
    return render_template('index.html')

@app.route('/sources')
def sources_page():
    return render_template('sources.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    surname = request.form['surname']
    patronymic = request.form['patronymic']
    email = request.form['email']
    cooling_type = request.form['cooling-type']
    feedback = request.form['feedback']
    option1 = request.form.get('option1')  
    option2 = request.form.get('option2')  
    gender = request.form.get('gender')
    image = request.files['image']
    
    options = []
    if option1:
        options.append("Ноутбук")
    if option2:
        options.append("Компьютер")
    

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        image_url = url_for('uploaded_file', filename=filename)
    else:
        image_url = None

    data = f'Name: {name}, Surname: {surname}, Patronymic: {patronymic}, Email: {email}, Cooling Type: {cooling_type}, Feedback: {feedback}, Options: {", ".join(options)}, Gender: {gender}, Image URL: {image_url}'
    save_data_to_file(data)

    return render_template('confirmation.html', name=name, surname=surname, patronymic=patronymic, email=email, cooling_type=cooling_type, feedback=feedback, options=options, gender=gender, image_url=image_url)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
