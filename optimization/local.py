from modules.utils import *
from modules.make_fisher_info_matrix import *
from modules.constOptFunc import *

def local_optimization(cRAT, cRTPCR, cIgG, p_vec):
  testCosts = [cRAT, cRTPCR, cIgG] #Basic cost of RAT, RT-PCR, IgG antibody tests

  dataDir = "./data/inputs"
  weps_val = 0.125

  # Make fisher inforamtion matrix
  mat = make_fisher_info_matrix(dataDir, testCosts)

  # minimize
  lenw = mat.get_lenw()
  weps = np.full(lenw, weps_val)
  v, v_vec = minimize_v(p_vec, mat, weps)

  #final solution
  solutionDF = get_make_solDF(mat, v_vec)

  return solutionDF, v

