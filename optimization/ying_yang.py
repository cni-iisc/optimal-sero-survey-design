##################################################################
# Ying-Yang: A gradient descent algorithm to find the worst case optimal point in sero-survey design.
# Author: Jagadish Midthala
# Dt: 21 March 2022
##################################################################

import time
import math
import csv
from modules.utils import *
from modules.make_fisher_info_matrix import *
from modules.constOptFunc import *
from scipy.special import softmax
float_formatter = "{:.5f}".format
np.set_printoptions(formatter={'float_kind':float_formatter})

def ying_yang_descent(cRAT, cRTPCR, cIgG, p1_start=0.16, p2_start=0.16, p3_start=0.10, specRAT=0.975, specRTPCR=0.97, specIGG=0.977, senRAT=0.75, senRTPCR=0.95, senIGG=0.921):
    testCosts = [cRAT, cRTPCR, cIgG] #Basic cost of RAT, RT-PCR, IgG antibody tests
    outputFile = './data/outputs/output_grid.tsv'
    dataDir = "./data/inputs"

    # Make fisher inforamtion matrix with specificities and specificities
    mat = make_fisher_info_matrix(dataDir, testCosts)
    mat.set_sensitivities(senRAT, senRTPCR, senIGG)
    mat.set_specificities(specRAT, specRTPCR, specIGG)


    # Uncoment this if believe that p3* = 0 (Conjecture)
    # p3_start = 0.0


    p_vec = p_shadow = np.array([p1_start,p2_start,p3_start])
    v_vec = np.array( [0.0, 0.0, 0.0, 0.5, 0.4, 0.1, 0.0] )
    
    ratio = 0.0
    iteration = 1
    accuracy_level = 5 

    while ratio < 1-10**-accuracy_level:
        va, v_vec  = minimize_v(p_vec, mat, v_vec)
        vb, p_shadow = maximize_p(v_vec, mat, p_shadow)
        vb=-vb

        ratio = va/vb
        beta = min(np.round(va/vb,3),0.88)

        print(iteration, ":", np.sum(p_vec), p_vec, p_shadow, v_vec, va, vb, va/vb)
        p_vec = np.add( ratio*p_vec, (1-ratio)*p_shadow)
        iteration += 1


