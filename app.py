from flask import Flask, render_template, request

import os
from werkzeug.utils import secure_filename
import prediction

upload_folder = os.path.join('static', 'uploads')
app = Flask(__name__)

app.config['UPLOAD'] = upload_folder


@app.route("/",methods=['POST','GET'])
def hello():
    if request.method == "POST":
        file = request.files.get('img',None)
        if file!=None:
            print('inside result')
            file.save(os.path.join(app.config['UPLOAD'], secure_filename(file.filename)))
            img = os.path.join(app.config['UPLOAD'], secure_filename(file.filename))
            patient, conf = prediction.prediction(img)
            if patient =="covid":
                pat_type = 'positive'
            else:
                pat_type = 'negative'
            return render_template("index.html",image = img, pat_type=pat_type, conf=conf)
        else:
            return render_template("index.html")

    else: 
        return render_template("index.html")


if __name__=="__main__":
    app.run()