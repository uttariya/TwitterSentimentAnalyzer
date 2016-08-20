from flask import Flask,request,render_template
from twitterExt import twitterext
from prepvalidationset import *
app = Flask(__name__)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/result',methods=['GET'])
def hello_world():
    x=request.args.get('field')
    z=twitterext(x)
    y=checker(z)
    return render_template('results.html',data=y)

if __name__ == '__main__':
    app.debug=True
    app.run()
