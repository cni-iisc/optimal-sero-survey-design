import numpy as np
import pandas as pd

def make_scenario_solution_matrix(ttypevalid, x):
    result = np.hstack((ttypevalid, np.append(0,x).reshape(8,1)))
    data = pd.DataFrame(x)
    zero = [0]
    zero_data = pd.DataFrame(zero)
    append_data = pd.concat([zero_data, data], ignore_index=True)
    precision_df = append_data.round(5)
    data_pd = pd.DataFrame(data)
    ttypeData = pd.DataFrame(ttypevalid)
    concat_df = pd.concat([ttypeData, precision_df], axis = 1, ignore_index = 'True')
    final_df = concat_df.rename(columns = {0:'RAT', 1:'RTPCR', 2:'AB', 3: 'Results'})
    return final_df

def make_p_combinations_specific():
    plist = []
    p1 = np.arange(0.01, 0.16, 0.01)
    p2 = np.arange(0.10, 0.51, 0.01)
    p3 = np.arange(0.00, 0.03, 0.01)
    for x in p1:
        for y in p2:
            for z in p3:
                plist.append([x, y, z])
    return plist

def get_final_solution(mat, v_vec, C):
    patternCost = np.array(mat.get_patternCost())
    solDF = make_scenario_solution_matrix(mat.get_ttypevalid(), v_vec)
    patternCost = np.insert(patternCost, 0, 1)
    print("total Budget:  ", C)
    print("patternCost:  ", patternCost)

    for index, row in solDF.iterrows():
        solDF.at[index,'componentCost'] = ( row['Results'] / patternCost[index] ) * C
    return solDF

def process_v_vector(outputFile):
    # Get final solution based on the max value for minimizing  a p-vector
    resultDF = pd.read_csv(outputFile, sep='\t')
    max_v_val = resultDF['v_val'].max()

    p_vec_out = resultDF.loc[resultDF['v_val'] == max_v_val, 'p_in'].values[0]
    v_vec_out = resultDF.loc[resultDF['v_val'] == max_v_val, 'v_vec'].values[0]
    del resultDF

    v_vec_out = v_vec_out.replace('\n', ' ').replace('  ', ' ')
    v_vec_out = v_vec_out[1:-1].split()
    v_vec_out = [float(x) for x in v_vec_out]

    return v_vec_out
