from scipy.optimize import minimize
from flask import Flask, render_template, request, jsonify
import numpy as np

T = 8 # Number of Igg tests
r = np.array([0.001,0.004,0.002, 0.001,0.000735,0.001,0.001,0.001])
c = np.array([0.85,0.85,0.75, 0.95,0.95,0.65,0.98])
s = np.array([0.95,0.85,0.85, 0.875,0.75,0.99,0.9])


f = np.array([1.0/T]*T) # Fraction of the budget allocated to test i
p = 0.5

def variance(p,f):
    pp = I_p = 0.0

    for i in range(T):
        pp = p*s[i] + (1-p)*(1-c[i])
        I_p += ( ((s[i]+c[i]-1)**2)*(1/pp + 1/(1-pp)) )*(f[i]/r[i])

    return 1.0/I_p

def variance_p(p):
    return -variance(p,f)

def variance_f(f):
    return variance(p,f)

def best_p(curf):
    # Initial point
    global f 
    f = curf
    p0 = 0.5
    #print( variance_p(p0) )
    b = (0.0,1.0)
    bnds = (b,)
    sol = minimize( variance_p, p0, method='SLSQP',\
                    bounds = bnds,
                    options={'disp': False, 'maxiter':1000, 'ftol':1e-10})
    return sol.fun, sol.x[0]


def constraint(f):
    s = 0.0
    for i in range(T):
        s += f[i]
    return s-1


def best_f(curp,cur_f):
    global p
    p = curp

    f0 = cur_f

    b = (0.0,1.0)
    bnds = (b,)*T
    con1 = {'type':'eq', 'fun': constraint}
    cons = [con1]

    sol = minimize( variance_f, f0, method='SLSQP',\
                    bounds = bnds,
                    constraints = cons,
                    options={'disp': False, 'maxiter':1000, 'ftol':1e-10})
    return sol.fun, sol.x


# Line search on p and pick the value that maximizes variance

def best_design():
    bestp = 0
    best_var = 0
    cur_f = bestf = f

    for pi in np.linspace(0,.99,100):
        var, cur_f = best_f(pi,cur_f)
        if best_var < var:
            best_var = var
            bestp = pi
            bestf = cur_f

    return( bestf.round(3).tolist(), np.sqrt(best_var) )


def set_variables(rr,cc,ss):
    global r,s,c,T,f
    r = rr
    c = cc
    s = ss
    T = len(r)
    f = np.array([1.0/T]*T) 
    return best_design()





app = Flask(__name__)

@app.route('/')
def index():
	return render_template('igg_form.html')


def tidy(r):
    try:
        r.remove('')
    except:
        pass
    l = np.array([])
    n = len(r)
    i = 0
    while i<n and r[i]!='':
        try:
            l = np.append(l, float(r[i]) )
        except:
            return []
        i += 1
    return l
    
def design(alloc,rup,budget):
    arr_kit = []
    for i in range(T):
        curkit = {}
        if alloc[i]>1e-8:
            curkit['id'] = str(i+1)
            curkit['num'] = str( int ((alloc[i]*budget)/rup[i] ) )
            curkit['alloc'] = rup[i]*int((alloc[i]*budget)/rup[i]) 
            arr_kit.append( curkit )
    print( arr_kit )
    return arr_kit


def invalid_input(r,c,s,budget):
    for x,y,z in zip(r,c,s):
        try:
            float(x)
            float(y)
            float(z)
            float(budget)
        except:
            return True

    return False

@app.route('/process', methods=['POST'])
def process():

    option =  int(request.form['opt'])
    print('Option',option)

    if option==1:
        try:
            budget = int( request.form['budget'] )
        except:
            return jsonify({'error' : 'Budget must be an integer!'})

    if option==2:
        try:
            margin =  float(request.form['m'])
            print("Margin:",margin)
        except:
            return jsonify({'error' : 'Margin must be between 0.005 and 0.01.'})



    r = request.form.getlist('r[]') 
    c = request.form.getlist('c[]') 
    s = request.form.getlist('s[]') 

    if tidy(r)==[] or tidy(c)==[] or tidy(s)==[]:
        return jsonify({'error' : 'Invalid input!'})

    r = rup = tidy( r )
    c = tidy( c )
    s = tidy( s )

    normalized_budget = sum(r)*10 # This 10 doesnt matter much, it's there  to get around numerical errors.
    r = r/normalized_budget
    # print("Budget is:", budget, "Sens:",s, "Spec:",c, "Cost",r)
    alloc, stddev = set_variables(r,s,c)
    normal_std = stddev.copy()


    if option==1:

        if budget < sum(r):
            return jsonify({'error' : 'Budget is too low!'})
        if budget > 100000001:
            return jsonify({'error' : 'Budget is too high'})

        arr_kit = design(alloc,rup,budget)
        stddev = normal_std/np.sqrt(budget/normalized_budget)
        return jsonify( {"kit":arr_kit, "stderror":stddev} )
    else:
        est_budget = normalized_budget*((stddev/margin)**2) 
        print("Estimated Budget:",est_budget)
        arr_kit = design(alloc,rup,int(est_budget))
        stddev = normal_std/np.sqrt(est_budget/normalized_budget)
        return jsonify( {"kit":arr_kit, "stderror":stddev} )


if __name__ == '__main__':
	app.run(debug=True)
    









