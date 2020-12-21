from modules.utils import *
from modules.make_fisher_info_matrix import *
from modules.constOptFunc import *

def local_optimization(cRAT, cRTPCR, cIgG, C):
  testCosts = [cRAT, cRTPCR, cIgG] #Basic cost of RAT, RT-PCR, IgG antibody tests

  dataDir = "./data/inputs"
  weps_val = 0.125

  # Set the predicted prevalence
  p_vec = [0.1, 0.3, 0.01]

  # Make fisher inforamtion matrix
  mat = make_fisher_info_matrix(dataDir, testCosts)

  # minimize
  lenw = mat.get_lenw()
  weps = np.full(lenw, weps_val)
  v, v_vec = minimize_v(p_vec, mat, weps)

  #final solution
  solutionDF = get_final_solution(mat, v_vec, C)

  return solutionDF

