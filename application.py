import pandas as pd
from babel.numbers import format_currency 
from flask import Flask, render_template, request, flash, url_for
from optimization.local import *
from optimization.grid_search import *

app = Flask(__name__, template_folder="template")
app.config['SECRET_KEY'] = 'a random string'


@app.route("/", methods=["POST", "GET"])
def init():
    z = 1.96 # For 95% confidence interval

    # default return values
    res = pd.DataFrame()
    budget = 500000
    totalCost = 0
    marginError = 0.05

    if request.method == "POST":
        # getting submitted values
        method = request.form.get('method')
        option = request.form.get('option') 
        cRAT = request.form.get('cRAT')
        cRTPCR = request.form.get('cRTPCR')
        cIgG = request.form.get('cIGG')
        inputBudget = request.form.get('budget')
        inputMargin = float(request.form.get('margin'))
        p1 = [float(x) for x in request.form.get('p1').split(" - ")]
        p2 = [float(x) for x in request.form.get('p2').split(" - ")]
        p3 = [float(x) for x in request.form.get('p3').split(" - ")]
        dEffect =  float(request.form.get('dEffect'))
       
        # convert to units of 1000 rupees
        cRAT = float(cRAT) / 1000
        cRTPCR = float(cRTPCR) / 1000
        cIgG = float(cIgG) / 1000
        inputBudget = float(inputBudget) / 1000
        
        # parameters
        C = 1
        m = 0
        objFunVal = 0

        if option == "error": #given budget compute margin of error
            C = inputBudget
            m = 0
            
        if option == "cost": #given margin of error compute budget
            C = 1
            m = inputMargin

        if method == 'local': # run locally-optimal design
            p_vec = [p1[0], p2[0], p3[0]]
            res, objFunVal = local_optimization(cRAT, cRTPCR, cIgG, p_vec)

        if method == 'grid': # run exhaustive search for worst-case design
            p1_start = p1[0]
            p1_end = p1[1] + 0.01
            p2_start = p2[0]
            p2_end = p2[1] + 0.01
            p3_start = p3[0]
            p3_end = p3[1] + 0.01
            res, objFunVal = exhaustive_search(cRAT, cRTPCR, cIgG, p1_start, p1_end, p2_start, p2_end, p3_start, p3_end)
                      
   
        if option == "error": #given budget compute margin of error
            marginError = z * (np.sqrt((objFunVal * dEffect) / C))
            budget = inputBudget

        if option == "cost": #given margin of error compute budget
            budget =  int(((z / m )**2) * (objFunVal * dEffect))
            marginError = inputMargin

        # prepare the output  
        res = get_final_solution(res, budget, cRAT, cRTPCR, cIgG)
        res = res.astype({'# Participants': int, "RT-PCR":int, "IgG Antibody":int, "RAT":int, 'Cost': int})
        res['Cost'] *= 1000 # convert to rupees
        budget *= 1000  # convert to rupees
        print(method, option, budget, marginError, inputMargin, inputBudget)

        totalCost = format_currency(res['Cost'].sum(), 'INR', locale='en_IN')
        res['Cost'] = res['Cost'].apply(lambda row: format_currency(row, 'INR', locale='en_IN'))
    return render_template('index.html', m=("%.5f" % marginError), mCost=budget, totalCost=totalCost, column_names=res.columns.values, row_data=list(res.values.tolist()), zip=zip)
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
