from app import app
from flask import render_template

@app.route('/')
def home():
    names = ['Shoha', "Dylan", "Christopher", "Alex", "Blair"]

    
    return render_template('index.html', my_list=names)



@app.route('/about')
def iCanNameThisAnything():
    return render_template('about.html')




@app.route('/api/v2/pokemon/')
def signMeUp():
    return {'hi' : "there"}


