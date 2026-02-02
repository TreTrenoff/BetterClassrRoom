#lib
from flask import Flask, render_template, request
import os

Template_Folder = os.path.join(os.getcwd(), "./html") 


app = Flask(__name__, template_folder=Template_Folder)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.get('data')
    return render_template('result.html', data=data)



#--------- RUN --------
if __name__ == '__main__':
    app.run(debug=True)
