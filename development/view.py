
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from pathlib import Path
import time
import os
import json
import sys
from subprocess import call


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'las'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Submit")

@app.route('/', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        
        # get the file data from frontend
        file = form.file.data
        
        # save the file name as a global variable, since we need to use it outside of this function
        global filename
        filename = file.filename
        
        # save the file under static/files folder
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(filename)))

        # las_file = Path("/Users/peinanwang/CS5500_Project/cs5500_geospatial_projects/development/static/files/" + file.filename)
        # 
        # while True:
        #     if las_file.is_file():
        #         break
        # 
        # time.sleep(60)
        
        # print a notification to the terminal when the file is saved successfully
        print("\nFile " + file.filename + " is submitted Successfully\n")
                      
    return render_template('/index.html', form=form)


@app.route("/visualize/", methods=['POST'])
def visualize_data():
    command = "python3 Visualize_in_browser/visualize_in_browser.py " +  filename
    call(command, shell=True)


'''
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return render_template('/index.html')
'''


'''
@app.route('/')
def new_page():
    return render_template('newpage.html')

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'


@app.route('/api/post/<int:post_id>', methods=['GET', 'POST'])
def show_certain_post(post_id):
    j_object = {"id":post_id,"content":"foo"}
    return json.dumps(j_object)

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")
'''

# This starts the flask app configured to listen on port 900
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5500))
    app.run(debug=True, host='0.0.0.0', port=port)


# curl -X GET http://localhost:800/api/post/42
# docker stop $(docker ps -a -q) && docker image build -t flask_docker . && docker run -p 5500:5500 -d flask_docker

