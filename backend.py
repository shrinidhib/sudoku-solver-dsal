from flask import Flask,render_template,request
from werkzeug.utils import secure_filename
import os

def execute(file_name):
    with open(file_name,'r') as f:
        code=f.read()
        exec(code)
app=Flask(__name__)
direc='/Users/balaji/Desktop/projects/sudoku/'

@app.route('/')
def upload_file():
    return render_template('index.html')

filename=''
@app.route('/upload', methods =['POST','GET'])
def upload():
    if request.method=='POST':
        f=request.files['file']
        global filename
        filename=f.filename
        filename=secure_filename(filename)
        print(filename)
        
        f.save(os.path.join('static/Images', filename))
        os.rename('static/Images/'+filename,'sudoku.png')
        execute('main.py')
        file=os.path.join(os.path.join('static','Images'),'final.png')
        return render_template('index.html',image=file)

    else:
        return render_template('index.html')


if __name__=='__main__':
    app.run(debug=True,port=5000)