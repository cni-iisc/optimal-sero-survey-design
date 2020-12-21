import time
import csv
from modules.utils import *
from modules.make_fisher_info_matrix import *
from modules.constOptFunc import *


def exhaustive_search(cRAT, cRTPCR, cIgG, C):
    testCosts = [cRAT, cRTPCR, cIgG] #Basic cost of RAT, RT-PCR, IgG antibody tests
    outputFile = './data/outputs/output_grid.tsv'
    dataDir = "./data/inputs"

    # Make fisher inforamtion matrix
    mat = make_fisher_info_matrix(dataDir, testCosts)

    weps = np.random.choice(50,7) #0.125
    weps = weps/(weps.sum() + 5)
    init_list = np.linspace(0,1,101).tolist()

    plist = make_p_combinations_specific()

    with open(outputFile, 'w') as csvfile:
        fieldnames = ['idx', 'v_val', 'p_in', 'v_vec', 'time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        for idx, p_vec in enumerate(plist):
            start_time = time.time()
            print(p_vec)

            condition = True
            while(condition):
                try:
                    v, v_vec = minimize_v(p_vec, mat, weps)
                except:
                    new_weps = np.random.choice(50,7) #0.125
                    new_weps = new_weps/(new_weps.sum() + 5)
                    v, v_vec = minimize_v(p_vec, mat, new_weps)
                    condition = False
                else:
                    condition = False

            print("--- %s seconds ---" % (time.time() - start_time))
            writer.writerow({
                "idx": idx,
                "v_val": v,
                "p_in": p_vec,
                "v_vec": v_vec,
                "time": (time.time() - start_time)
            })

    v_vec_out = process_v_vector(outputFile)
    return get_final_solution(mat, v_vec_out, C)