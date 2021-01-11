import numpy as np
import pandas as pd

class make_fisher_info_matrix():
  def __init__(self, dataDir, testCosts):
    self.txset = pd.read_csv(f"{ dataDir }/ratrtpcrabvec.csv")
    self.highs = pd.read_csv(f"{ dataDir }/ratrtpcrabhighs.csv")
    self.highs = self.highs.drop(columns=['Infection.State']).to_numpy() 

    self.testCosts = testCosts

    self.ttypevalid, self.patternCost = self.getCosting()
    self.patternCost = self.patternCost[1:]

    self.lenw = len(self.patternCost)

  def get_lenw(self):
    return self.lenw

  def get_patternCost(self):
    return self.patternCost
  
  def get_ttypevalid(self):
    return self.ttypevalid

  def getCosting(self):
    ttypevalid = self.txset.copy()
    #null value based values
    ttypevalid['RAT'] = 1 - ttypevalid['RAT'].apply(lambda x: 1 if pd.isna(x) else 0) 
    ttypevalid['RTPCR'] = 1 - ttypevalid['RTPCR'].apply(lambda x: 1 if pd.isna(x) else 0)
    ttypevalid['AB'] = 1 - ttypevalid['AB'].apply(lambda x: 1 if pd.isna(x) else 0)

    ttypevalid = ttypevalid.drop_duplicates() # get unique rows
    ttypevalid = ttypevalid.drop(columns=['Test.Type']).to_numpy() #make a 2D matrix

    return ttypevalid, np.matmul(ttypevalid, np.array(self.testCosts)) #matrix multiplilcation

  # # This function estimates q_t(x;p), the probability of seeing test outcome x
  # # when test type is t and the disease prevalence vector is p.
  # # p = c(p[1], p[2], p[3]). ActiveInfection, ActiveABonly, ActiveForBoth
  # # Last state carries the remaining probability.
  def qxp(self, x, p):
      # Structure of x and p : x = ("0", "1", ""), p = (0.1, 0.2, 0.3)x
      prod = [1, 1, 1, 1]
      # col = highs.columns.values.tolist()

      ##0=RAT,1=RTPCR,2=AB
      Spec = [0.975,0.97,0.977]
      Sen  = [0.5,0.95,0.921]

      for j in range(3):
          if(x[j] == "0.0"):
              for i in range(4):
                  # For state i, test j, if correct response highs[i,j] is 1, 
                  # this is a sensitivity error. 
                  # If correct response is 0, this is correct specificity.
                  prod[i] = (prod[i])*(self.highs[i, j]*(1-Sen[j]) + (1-self.highs[i, j])*Spec[j])

          if(x[j] == "1.0"):
              for i in range(4):
                  # See explanation above
                  prod[i] = prod[i]*(self.highs[i, j]*(Sen[j]) + (1-self.highs[i, j])*(1 - Spec[j]))

      r = np.append(p, 1-sum(p))
      prod = np.array(prod)
      # log-probability, gradients[3], probability
      return [np.log(prod.dot(r)), prod[0]-prod[3], prod[1]-prod[3], prod[2]-prod[3], prod.dot(r)]

  # ###Fisher information for a test pattern
  def getPatternFisherInfo(self, p, t):
      x = self.txset.copy().drop(columns=['Test.Type'])
      # Compute the Fisher information matrix, weighted
      I = np.diag([0.0, 0.0, 0.0])
      # if t in [1, 3, 5, 7]: #consider only cases with RT-PCR tests
      for i in range(3):
          for j in range(i,3):
              sx = x.loc[self.txset['Test.Type'] == t+1]
              v2 = 0
              for k in range(sx.shape[0]):
                  y = sx.iloc[k,].values.astype(str).tolist()
                  Q = self.qxp(y, p) #Q[2:4] are gradients. Q[5] is probability
                  v2 = v2 + ((Q[1 + i]) * Q[1 + j]) / (Q[4])
              I[i, j] = v2
              I[j, i] = v2
      return I

  ###Weighted Fisher information
  def getWeightedFisherInfo(self, wsub, p):
      #Initialise to uniform test patterns. Ensure interior point, to begin.
      ttype  = self.txset['Test.Type'].unique().tolist()
      w = np.append(0, np.array(wsub))
      I = np.diag([0.0, 0.0, 0.0])
      for t in range(1, len(ttype)):
          widx = t - 1
          I = I + (w[t] / self.patternCost[widx]) * self.getPatternFisherInfo(p, t)
      return I
