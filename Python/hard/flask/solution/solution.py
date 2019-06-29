
#import the used libraries
from flask import Flask, session, render_template, Blueprint, url_for, request,redirect, flash
import os
from werkzeug.utils import secure_filename

#register the app and create a session when the user comes to our page
app = Flask(__name__)
app.secret_key = "super secret key"

#register the sub url upload, generated by the method uopload_file
#The url also has the methods post and get
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    #wenn die from submited wurde/eine file hochgeladen wurde
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            #save the file to a folder in this directory
            file.save(os.path.join(os.path.dirname(os.path.abspath(__file__))+"/upload/", filename))
            return redirect(url_for('upload_file',
                                    filename=filename))
    #when this side is loaded, display the following html structure
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

#register the index url and all undefined urls
@app.route('/')
@app.route('/<name>')
def index(name=None):
    #render the html template index and give the parameter name from the url to it
    return render_template('index.html', name=name)

#register the url redirect, which redirects to google
@app.route('/redirect')
def redirection():
    return redirect("http://www.google.de")

#register the url quiz, which handles also post and get requests
@app.route("/quiz", methods=("GET", "POST"))
def quiz():
    #wenn der button submit gedrueckt wurde
    if request.method=="POST":
        #Antwort aus dem Textfeld bekommen
        answer = request.form["answer"]
        #wenn die Antwort sieben ist zeige die message Correct, sonst Wrong
        if answer == "7" or answer == "sieben":
            flash("Correct!")
        else:
            flash("Wrong answer try again...")
    #wenn die Seite geoeffnet wird lade das quiz html template
    return render_template('quiz.html')