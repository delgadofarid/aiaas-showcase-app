# from flask import Flask,abort,render_template,request,redirect,url_for
from flask import Flask, flash, request, redirect, url_for, render_template, make_response, send_from_directory
from werkzeug.utils import secure_filename
import os
import time

from app.processor import ImageProcessor

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'mysecretfortesting'
app.config['SESSION_TYPE'] = 'filesystem'

image_processor = ImageProcessor()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['GET','POST'])
def home():
    if request.method =='POST':
        uploaded_files = request.files.getlist("file[]")
        uid = str(time.time())
        print(f"Saving files under: ./uploads/{uid}...")
        target_dir = os.path.join('src', 'app', app.config['UPLOAD_FOLDER'], uid)
        os.mkdir(target_dir)
        processed = list()
        if uploaded_files:
            for file in uploaded_files:
                filename = secure_filename(file.filename)
                target_path = os.path.join(target_dir, filename)
                file.save(target_path)
                task = request.form.get('task')
                proc_img = image_processor.process_image(target_path, task)
                proc_img.filename = os.path.basename(proc_img.path)
                proc_img.parent = uid
                proc_img.task = task
                processed.append(proc_img)
                print(f"{target_path} processed ...")
            tuple_size = 2
            tuple_list = [processed[n:n+tuple_size] for n in range(0, len(processed), tuple_size)]
            return render_template('file_details.html', images=tuple_list)
    
    tasks=["face", "label", "landmark", "logo", "object", "text"]
    tareas=["rostros", "escenas aleatorias", "puntos de referencia", "logos", "objetos", "textos"]
    return render_template('file_upload.html', tasks=list(zip(tasks, tareas)))

@app.route('/uploads/<parent>/<filename>')
def download_file(parent, filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], os.path.join(parent, filename))