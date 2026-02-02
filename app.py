from flask import Flask, render_template, request

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)