# Main program for local c-optimal design (illustrations of paper's Theorem 1)
##########################
#Set workking directory
#Source functions
#Set cost
#Set patternCost
#Set p
#Set sensitivity
#Set specificity
#Initialise
#Run optimiations
##########################

# Set directory
setwd("./")

# Source functions
source("./testAllocationOptimisation.r")

# Set cost of RAT, RT-PCR, IgG antibody in 1000 rupees
# Uncomment the line of interest and comment the others.
#testCosts = c(0.45, 1.6, 0.30)
#testCosts = c(0.45, 1.0, 0.30)
testCosts = c(0.45, 0.1, 0.30)

# Set cost of test patterns. Remember to remove the top row.
patternCost = getCosting(testCosts)
patternCost = patternCost[-1]

# Set the guessed prevalence for local c-optimal design
p = c(0.1,0.3,0.01)
# The following was the worst case (Theorem 2) obtained via a grid search.
# p = c(0.06,0.45,0)

## Global sensitivity and specificity
## 1=RAT,2=RTPCR,3=AB
Spec = c(0.975,0.97,0.977)
Sen  = c(0.5,0.95,0.921)

# Modifications for the paper's Theorem 4 calculations
#Sen  = c(0.47,0.95,0.921)
#Sen  = c(0.68,0.95,0.921)

#Initialise to uniform test patterns. Ensure interior point, to begin.
weps = 0.1
lenw = length(patternCost)
initw = rep(weps, lenw)

# Local c-optimal allocation
w2 = constrOptim(initw, varfun, vargrad, constrM, constrval, control = list(abstol=1e-12), outer.iterations=2000, outer.eps=1e-12)

# KKT conditions
lambda = rep(0,lenw)
for (widx in 1:lenw) {
  lambda[widx] = kktcheck(w2$par,widx+1)
}

# Reload txset and testtypes for printing
ttypevalid = cbind(txset$Test.Type, 1-as.numeric(is.na(txset$RAT)), 1-as.numeric(is.na(txset$RTPCR)), 1-as.numeric(is.na(txset$AB)))
ttypevalid = unique(ttypevalid)

# Budget in 1000 rupee units
C = 10000
finalout = cbind(ttypevalid, c(0,round(lambda,5)), c(0,round(w2$par,5)), c(0,round(C*(w2$par/patternCost),0)))
finalout
