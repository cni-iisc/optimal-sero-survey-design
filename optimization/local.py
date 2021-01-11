from modules.utils import *
from modules.make_fisher_info_matrix import *
from modules.constOptFunc import *

def local_optimization(cRAT, cRTPCR, cIgG, p_vec):
  testCosts = [cRAT, cRTPCR, cIgG] #Basic cost of RAT, RT-PCR, IgG antibody tests

  dataDir = "./data/inputs"
  weps_val = 0.125

  # Make fisher inforamtion matrix with specificities and specificities
  specRAT = 0.975
  specRTPCR =0.97
  specIGG = 0.977

  senRAT = 0.5
  senRTPCR = 0.95
  senIGG = 0.921

  mat = make_fisher_info_matrix(dataDir, testCosts)
  mat.set_sensitivities(senRAT, senRTPCR, senIGG)
  mat.set_specificities(specRAT, specRTPCR, specIGG)

  # minimize
  lenw = mat.get_lenw()
  weps = np.full(lenw, weps_val)
  v, v_vec = minimize_v(p_vec, mat, weps)

  #final solution
  solutionDF = get_make_solDF(mat, v_vec)

  return solutionDF, v

