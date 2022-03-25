##################################################################
# Yin-Yang: A gradient descent algorithm to find the worst case optimal point in sero-survey design.
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
float_formatter = "{:.3f}".format
np.set_printoptions(formatter={'float_kind':float_formatter},precision=3)


def save_result(p_vec,v_vec,ratio):

    # Save the final point
    with open('equilibrium_point.npy','wb') as f:
        np.save(f,p_vec)
        np.save(f,v_vec)
        np.save(f,np.array([ratio]))
    
    float_formatter = "{:.12f}".format
    np.set_printoptions(formatter={'float_kind':float_formatter},precision=3)

    with open('equilibrium_point.npy','rb') as f:
        print("Optimal responses:")
        print(np.load(f), np.load(f),np.load(f) )

def scorecard(iteration=0,p_vec=[],v_vec=[],va=0,vb=0,weight=1,header=False):
    if header==True:
        header = [ 't', 'Bob (Max. player): p_t', 'Alice (Min. player): v_t' ,  'Alice' , 'Bob', 'Approx. Nash' ]
        print( "-"*125+"\n", "{:^4s} | {:^14s}  | {:^46s} | {:^10s} | {:^10s} | {:^15s}".format(*header), end="\n"+"-"*125+"\n" )
    else:
        print("  {:<4}".format(iteration),end="")
        print("|", "  ", p_vec, " |  ", v_vec, " | ", "%.6f"%va, " | ", "%.6f"%vb , " | ", "%.12f"%(va/vb))




def yin_yang_descent(cRAT, cRTPCR, cIgG, p1_start=0.16, p2_start=0.16, p3_start=0.10, 
        specRAT=0.975, specRTPCR=0.97, specIGG=0.977, senRAT=0.51, senRTPCR=0.95, senIGG=0.921):
    testCosts = [cRAT, cRTPCR, cIgG] #Basic cost of RAT, RT-PCR, IgG antibody tests
    outputFile = './data/outputs/output_grid.tsv'
    dataDir = "./data/inputs"

    # Make fisher inforamtion matrix with specificities and specificities
    mat = make_fisher_info_matrix(dataDir, testCosts)
    mat.set_sensitivities(senRAT, senRTPCR, senIGG)
    mat.set_specificities(specRAT, specRTPCR, specIGG)


    # Solving the optimization problem using a min-max game 

    p_vec = p_shadow = np.array( [p1_start,p2_start,p3_start] )
    v_vec = np.array( [0.0, 0.0, 0.0, 0.5, 0.4, 0.1, 0.0] )
    ratio = 0.0
    accuracy_level = 3  # 3 correspnds to 0.999-approx  
    iteration = 1


    scorecard([],header=True)

    weight = 1
    prev_ratio = 1
    tolerance = 1e-6

    while ratio < 1-10**-accuracy_level and iteration<100:

        va, v_vec  = minimize_v(p_vec, mat, v_vec, tolerance)
        vb, p_shadow = maximize_p(v_vec, mat, p_shadow, tolerance)

        ratio = va/vb

        scorecard(iteration,p_vec,v_vec,va,vb,ratio,header=False)

        p_vec = np.add( ratio*p_vec, (1-ratio)*p_shadow)

        prev_ratio = ratio
        tolerance = vb-va
        iteration += 1





