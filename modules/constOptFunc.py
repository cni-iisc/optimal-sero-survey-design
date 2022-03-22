import numpy as np
from scipy.optimize import minimize

lastw_vec = np.array([])

# # Interest is in minimising the u^T I(w)^-1 u.
def varfun(min_vec, const_vec, mat):
    I = mat.getWeightedFisherInfo(min_vec, const_vec)
    u = np.array([1.0, 1.0, 1.0])
    J = np.linalg.inv(I) #getting inverse of matrix I
    # Matrix product u^T J u
    return np.matmul( np.matmul(u.transpose(), J), u)

def varfun_max(const_vec, max_vec, mat):
    I = mat.getWeightedFisherInfo(max_vec, const_vec)
    u = np.array([1.0, 1.0, 1.0])
    J = np.linalg.inv(I) #getting inverse of matrix I
    # Matrix product u^T J u
    return -1 * np.matmul( np.matmul(u.transpose(), J), u)

def minimize_v(p, mat, weps):
    #Initialise to uniform test patterns. Ensure interior point, to begin.
    lenw = mat.get_lenw()
    initw = weps

    M = np.full(lenw, 1)
    lb = np.full(lenw, 0)
    ub = np.full(lenw, 1)

    def constrFun(wsub):
        return 1 - M.dot(wsub)

    const = {
        'type': 'ineq',
        'fun': constrFun
    }

    bounds = ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1))

    # Optimise
    a = minimize(varfun, initw, args=(p, mat), method='SLSQP',  bounds=bounds, constraints=(const), tol=1e-6, options={'ftol': 1e-6,  'eps': 1e-6, 'maxiter': 1000, 'disp': False})


    v = a.fun
    return v, a.x

def maximize_p(v_vec, mat, p_vec):
    #Initialise to uniform test patterns. Ensure interior point, to begin.
    lenp = 3
    #initp = np.full(lenp, 0.33)
    initp = p_vec

    M = np.full(lenp, 1)
    lb = np.full(lenp, 0)
    ub = np.full(lenp, 1)

    def constrFun(p):
        return 1 - M.dot(p)

    const = {
        'type': 'ineq',
        'fun': constrFun
    }

    bounds = ((0, 1), (0, 1), (0, 1))

    # Optimise
    a = minimize(varfun_max, initp, args=(v_vec, mat), method='SLSQP',  bounds=bounds, constraints=(const), tol=1e-6, options={'ftol': 1e-6,  'eps': 1e-6, 'maxiter': 1000, 'disp': False})

    v = a.fun
    return -v, a.x
