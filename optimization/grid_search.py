import time
import csv
from modules.utils import *
from modules.make_fisher_info_matrix import *
from modules.constOptFunc import *


def exhaustive_search(cRAT, cRTPCR, cIgG, p1_start=0.01, p1_end=0.16, p2_start=0.10, p2_end=0.51, p3_start=0.00, p3_end=0.03):
    testCosts = [cRAT, cRTPCR, cIgG] #Basic cost of RAT, RT-PCR, IgG antibody tests
    outputFile = './data/outputs/output_grid.tsv'
    dataDir = "./data/inputs"

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

    weps = np.random.choice(50,7) #0.125
    weps = weps/(weps.sum() + 5)
    init_list = np.linspace(0,1,101).tolist()
    progress = 0
    plist = make_p_combinations_specific(p1_start, p1_end, p2_start, p2_end, p3_start, p3_end)
    with open(outputFile, 'w') as csvfile:
        fieldnames = ['idx', 'v_val', 'p_in', 'v_vec', 'time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        for idx, p_vec in enumerate(plist):
            start_time = time.time()
            print(p_vec)

            condition = True
            progress = idx
            while(condition and sum(p_vec) <= 1):
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

    v_vec_out, max_v_val = process_v_vector(outputFile)
    return get_make_solDF(mat, v_vec_out), max_v_val
