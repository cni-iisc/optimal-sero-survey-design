# testAllocationOptimisation.r

library(matrixcalc)                                        
#library(matlib)
###

# Cost of RAT, RT-PCR, IgG antibody in 1000 rupees
testCosts = c(0.45, 1.6, 0.30)

# Set the guessed prevalence for local c-optimal design
p = c(0.1,0.3,0.01)

# The set of test types and test outcomes
txset= read.csv("../data/inputs/ratrtpcrabvec.csv", header=T)

# Diseasestate - response map. Read and delete the row names.
highs= read.csv("../data/inputs/ratrtpcrabhighs.csv", header=T)
highs = highs[-c(1)]

## Global sensitivity and specificity
## 1=RAT,2=RTPCR,3=AB
Spec = c(0.975,0.97,0.977)
Sen  = c(0.5,0.95,0.921)



# This function estimates q_t(x;p), the probability of seeing test outcome x
# when test type is t and the disease prevalence vector is p.
# p = c(p[1], p[2], p[3]). ActiveInfection, ActiveABonly, ActiveForBoth
# Last state carries the remaining probability.
qxp = function(x,p){
  # Structure of x and p : x = ("0", "1", ""), p = (0.1, 0.2, 0.3)x
  output = 0
  prod = c(1,1,1,1)
  for(j in 1:3){
    if(x[j]=="0"){
      for(i in 1:4) {
        # For state i, test j, if correct response highs[i,j] is 1, 
        # this is a sensitivity error. 
        # If correct response is 0, this is correct specificity.
        prod[i] = prod[i]*(highs[i,j]*(1-Sen[j]) + (1-highs[i,j])*Spec[j])
      }
    }
    if(x[j]=="1"){
      for(i in 1:4) {
        # See explanation above
        prod[i] = prod[i]*(highs[i,j]*Sen[j] + (1-highs[i,j])*(1-Spec[j]))
      }
    }
  }
  r = c(p, 1-sum(p))
  # log-probability, gradients[3], probability
  output=c(log(sum(prod*r)), prod[1]-prod[4], prod[2]-prod[4], prod[3]-prod[4], sum(prod*r))
}

###Fisher information for a test pattern
getPatternFisherInfo = function(p, t){
  x = txset[-c(1)]
  # Compute the Fisher information matrix, weighted
  I = diag(c(0,0,0))
  #if ((t==4) | (t==6) | (t==8)) { # Uncomment this line if RTPCR is free.
  for(i in 1:3) {
    for (j in i:3) {
      sx = subset(x, txset$Test.Type==t)
      v2=0
      for(k in 1:nrow(sx)){
          y =c(sx[k,])
          Q=qxp(y,p) #Q[2:4] are gradients. Q[5] is probability
          v2 = v2 + ((Q[1+i])*Q[1+j])/(Q[5])
      }
      I[i,j] = v2
      I[j,i] = v2
    }
  }
  #} # Uncomment this line if RTPCR is free.
  out = I
}

###Weighted Fisher information
getWeightedFisherInfo = function(p, wsub, pcost){

  # Identify test types
  ttype = unique(txset$Test.Type)
  w = c(0,wsub)

  # t=1, initialisation  
  I = diag(c(0,0,0))
  for(t in 2:length(ttype)){
    widx = t-1
    I = I + w[t]*getPatternFisherInfo(p,t)/pcost[widx]
  }
  out = I
}

getCosting = function(costvec){
  ttypevalid = cbind(txset$Test.Type, 1-as.numeric(is.na(txset$RAT)), 1-as.numeric(is.na(txset$RTPCR)), 1-as.numeric(is.na(txset$AB)))
  ttypevalid = unique(ttypevalid)
  out = ttypevalid[,-1] %*% costvec
}

varfun = function(wsub){
  I = getWeightedFisherInfo(p,wsub,patternCost)
  J = matrix.inverse(I)
  u = c(1,1,1)
  out = t(u) %*% J %*% u
  out
}

vargrad = function(wsub){
  I = getWeightedFisherInfo(p,wsub,patternCost)
  J = matrix.inverse(I)
  u = c(1,1,1)
  mygrad = rep(0,length(wsub))
  tmax = length(wsub)+1 # wsub and w = (0, wsub)
  for (widx in 1:length(wsub)) {
    # Index of pattern is 1 more than idx, since the first one is dropped
    t = widx+1
    patternFisherInfoGradWeighted = getPatternFisherInfo(p,t)/patternCost[widx]
    mygrad[widx] = -t(u) %*% J %*% patternFisherInfoGradWeighted %*% J %*% u
  }
  out = mygrad
}


patternCost = getCosting(testCosts)
patternCost = patternCost[-1]

#Initialise to uniform test patterns. Ensure interior point, to begin.
weps = 0.1
lenw = length(patternCost)
initw = rep(weps, lenw)

# Linear inequality constraint: M w \geq b
constrM = diag(rep(1,lenw))
constrM = rbind(constrM, -rep(1,lenw))

# Vector b for constraint
constrval = c(rep(0,lenw), -1)
 

constrg = function(wsub){
  out = -(constrM %*% wsub - constrval)
}

constrgJacobian = function(wsub) {
  out = -constrM
}

objfun = function(wsub){
  return( list( "objective" = varfun(wsub),
                "gradient" = vargrad(wsub) ) )
}

constrfun = function(wsub){
  constr = constrg(wsub)
  grad = constrgJacobian(wsub)
  return( list( "constraints" = constr, "jacobian" = grad ) )
}

kktcheck = function(wsub,t) {
  I = getWeightedFisherInfo(p,wsub,patternCost)
  J = matrix.inverse(I)
  u = c(1,1,1)
  # Assume t>1
  widx = t-1
  patternFisherInfoGradWeighted = getPatternFisherInfo(p,t)/patternCost[widx]
  out1 = t(u) %*% J %*% patternFisherInfoGradWeighted %*% J %*% u
  out2 = t(u) %*% J %*% u
  out = out1-out2
}
