from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('form.html')


def tidy(r):
    try:
        r.remove('')
    except:
        pass
    l = np.array([])
    n = len(r)
    i = 0
    while i<n and r[i]!='':
        l = np.append(l, float(r[i]) )
        i += 1
    return l
    

@app.route('/process', methods=['POST'])
def process():
    print('Processing')
    r = tidy( request.form.getlist('r[]') )
    c = tidy( request.form.getlist('c[]') )
    s = tidy( request.form.getlist('s[]') )
    budget = request.form['budget']
    print("Budget is:", budget)
    print("Sens :", s)
    print("Spec :", c)
    print("Cost :", r)

    if r[0]:
        return jsonify({'budget' : r, 'rupees': r[0]})

    return jsonify({'error' : 'Missing data!'})

if __name__ == '__main__':
	app.run(debug=True)
    


