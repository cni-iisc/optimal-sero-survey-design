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


def scorecard(iteration=0,p_vec=[],v_vec=[],va=0,vb=0,weight=1,header=False):
    if header==True:
        header = [ 't', 'Bob (Min. player): p_t', 'Alice (Max. player): v_t' ,  'Bob' , 'Alice', 'Approx. Nash' ]
        print( "-"*125+"\n", "{:^4s} | {:^14s}  | {:^46s} | {:^10s} | {:^10s} | {:^15s}".format(*header), end="\n"+"-"*125+"\n" )
    else:
        print("  {:<4}".format(iteration),end="")
        print("|", "  ", p_vec, " |  ", v_vec, " | ", "%.6f"%va, " | ", "%.6f"%vb , " | ", "%.12f"%(va/vb), " | ", weight)




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


    p_vec = p_shadow = np.array( [p1_start,p2_start,p3_start] )
    v_vec = np.array( [0.0, 0.0, 0.0, 0.5, 0.4, 0.1, 0.0] )
    ratio = 0.0
    accuracy_level = 10  # 4 correspnds to 0.9999-aprox  
    iteration = 1


    scorecard([],header=True)

    weight = 1
    prev_ratio = 1

    while ratio < 1-10**-accuracy_level and iteration<3000:
        va, v_vec  = minimize_v(p_vec, mat, v_vec)
        vb, p_shadow = maximize_p(v_vec, mat, p_shadow)
        ratio = va/vb
        scorecard(iteration,p_vec,v_vec,va,vb,ratio,header=False)

        #np.array_str(v_vec,precision=2,float_formatter=2), " ", va, " " , vb, " ",ratio  )

        p_vec = np.add( ratio*p_vec, (1-ratio)*p_shadow)
        prev_ratio = ratio
        iteration += 1


    with open('equilibrium_point.npy','wb') as f:
        np.save(f,p_vec)
        np.save(f,v_vec)
        np.save(f,np.array([ratio]))
    
    float_formatter = "{:.12f}".format
    np.set_printoptions(formatter={'float_kind':float_formatter},precision=3)

    with open('equilibrium_point.npy','rb') as f:
        print(np.load(f), np.load(f),np.load(f) )





