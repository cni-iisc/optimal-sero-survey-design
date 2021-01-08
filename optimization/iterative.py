import csv
from modules.utils import *
from modules.make_fisher_info_matrix import *
from modules.constOptFunc import *

cRAT = 0.5 #Test cost in thousand rupee units
cRTPCR = 1.2
cIgG =  0.3
testCosts = [cRAT, cRTPCR, cIgG] #Basic cost of RAT, RT-PCR, IgG antibody tests

dataDir = "./data/input"
outputFile = "./data/outputs/output_minmax.tsv"
threshold = 0.011

# Set the predicted prevalence
p_vec = [0.1, 0.3, 0.01]

# Make fisher inforamtion matrix
mat = make_fisher_info_matrix(dataDir, testCosts)

weps = np.random.choice(50,7) #0.125
weps = weps/(weps.sum() + 5)

iteration = 0
circle_iteration = 0
v_prev = 0

with open(outputFile, 'w') as csvfile:
    fieldnames = ['idx', 'v_val', 'v_vec', 'p_in', 'p_out']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()

    while True:
      print(iteration)

      condition = True
      while(condition):
          try:
              v, v_vec = minimize_v(p_vec, mat, weps)
          except:
              new_weps = np.random.choice(50,7) #0.125
              new_weps = new_weps/(new_weps.sum() + 5)
              v, v_vec = minimize_v(p_vec, mat, new_weps)
          else:
              condition = False
      p_val, p_out = maximize_p(v_vec, mat)

      if (np.abs(v_prev - v) <= threshold):
        #condition for early stop
        print(f"Stopping.. \n\n\ v-value = {v} p-vector = {p_vec}")
        writer.writerow({
            "idx": iteration,
            "v_val": v,
            "v_vec": v_vec,
            "p_in": p_vec,
            "p_out": p_out
        })
        break
      if np.abs(v) == np.abs(v_prev):
        circle_iteration += 1
        if circle_iteration > 2:
          writer.writerow({
              "idx": iteration,
              "v_val": v,
              "v_vec": v_vec,
              "p_in": p_vec,
              "p_out": p_out
          })
          break

      writer.writerow({
            "idx": iteration,
            "v_val": v,
            "v_vec": v_vec,
            "p_in": p_vec,
            "p_out": p_out
        })
      iteration += 1
      v_prev = v
      p_vec = p_out
