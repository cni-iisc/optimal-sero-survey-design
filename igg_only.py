import numpy as np
from scipy.optimize import minimize

T = 6 # Number of Igg tests


r = np.array([0.01,0.04,0.02, 0.013,0.009,0.01])
c = np.array([0.75,0.85,0.75, 0.95,0.95,0.65])
s = np.array([0.8,0.85,0.85, 0.875,0.75,0.99])
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
                    options={'disp': False, 'maxiter':1000, 'ftol':1e-9})
    return sol.fun, sol.x[0]


def constraint(f):
    s = 0.0
    for i in range(T):
        s += f[i]
    return s-1


def best_f(curp):
    global p
    p = curp

    f0 = [1.0/T]*T
    #print( variance_f(f0) )

    b = (0.0,1.0)
    bnds = (b,)*T
    con1 = {'type':'eq', 'fun': constraint}
    cons = [con1]

    sol = minimize( variance_f, f0, method='SLSQP',\
                    bounds = bnds,
                    constraints = cons,
                    options={'disp': False, 'maxiter':100, 'ftol':1e-8})
    return sol.fun, sol.x


# Line search on p and pick the value that maximizes variance


best_p = 0
best_var = 0
bestf = f

for pi in np.linspace(0,.99,100):
    var, cur_f = best_f(pi)
    if best_var < var:
        best_var = var
        best_p = pi
        bestf = cur_f
print( best_p, bestf.round(2), best_var )



'''
# Gradient descent (both this and linesearch give the same solution)


p_vec = p_shadow = 0.5
v_vec = f

ratio = 0.0
iteration = 1
tolerance = 1e-4

while ratio < .999 and iteration<1000:
    va, v_vec  = best_f(p_vec)
    vb, p_shadow = best_p(v_vec)
    ratio = -va/vb
#    print(iteration, ":", p_vec, v_vec.round(2), va, vb, "ratio:", ratio)
    p_vec = np.add( ratio*p_vec, (1-ratio)*p_shadow)
    iteration += 1

print("Solution")
print (p_vec)
print (v_vec)
print ( best_f(p_vec)[0] )


print("*"*100)
'''


