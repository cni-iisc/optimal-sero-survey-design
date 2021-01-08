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
    final_df = concat_df.rename(columns = {0:'RAT', 1:'RT-PCR', 2:'IgG Antibody', 3: '# Tests'})
    return final_df

def make_p_combinations_specific(p1_start, p1_end, p2_start, p2_end, p3_start, p3_end):
    plist = []
    p1 = np.arange(p1_start, p1_end, 0.01)
    p2 = np.arange(p2_start, p2_end, 0.01)
    p3 = np.arange(p3_start, p3_end, 0.01) 
    for x in p1:
        for y in p2:
            for z in p3:
                plist.append([x, y, z])
    return plist

def get_make_solDF(mat, v_vec):
    patternCost = np.array(mat.get_patternCost())
    solDF = make_scenario_solution_matrix(mat.get_ttypevalid(), v_vec)
    patternCost = np.insert(patternCost, 0, 1)

    for index, row in solDF.iterrows():
        solDF.at[index,'# Participants'] = (row['# Tests'] / patternCost[index])
    return solDF[['RAT', 'RT-PCR', 'IgG Antibody', '# Participants']]

def get_final_solution(solDF, C, cRAT, cRTPCR, cIgG):
    solDF['# Participants'] = solDF['# Participants'].apply(lambda row: np.floor(row * C))
    solDF['Cost'] = solDF.apply(lambda row: row['# Participants'] * (row['RAT']*cRAT + row['RT-PCR']*cRTPCR + row['IgG Antibody']*cIgG), axis=1)
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

    return v_vec_out, max_v_val
