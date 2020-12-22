# Main program for local optimisation
##########################
#Set workking directory
#Source functions
#Set cost
#Set patternCost
#Set sensitivity
#Set specificity
#Set p range
#Set restricted t
#Initialise
#Run optimisations
##########################

# Set directory
setwd("./")

# Source functions
source("./testAllocationOptimisation.r")

# Set cost of RAT, RT-PCR, IgG antibody in 1000 rupees
#testCosts = c(0.45, 1.6, 0.30)
testCosts = c(0.45, 0.1, 0.30)

# Set cost of test patterns. Remember to remove the top row.
patternCost = getCosting(testCosts)
patternCost = patternCost[-1]

## Global sensitivity and specificity
## 1=RAT,2=RTPCR,3=AB
Spec = c(0.975,0.97,0.977)
Sen  = c(0.5,0.95,0.921)


# Set the guessed prevalence for local c-optimal design
p = c(0.1,0.3,0.01)

# Set p range
p1set = c(1:15)/100
p2set = c(10:50)/100
p3set = c(0:2)/100
# p1set = c(50)/100
# p2set = c(5)/100
# p3set = c(0)/100
t = 6 #Focus only on RTPCR and AB
resultM = t(c(0,0,0,0))

for (p1 in p1set) {
  for (p2 in p2set) {
    for (p3 in p3set) {
      u = c(1,1,1)
      p = c(p1,p2,p3)
      localI = getPatternFisherInfo(p,t)
      # Uncomment these lines to run for calculated worst case.
      # r=0.025141
      # localI1 = getPatternFisherInfo(p,t-1)
      # localI = (1-r)*localI+r*localI1
      localJ = matrix.inverse(localI)
      var = (t(u) %*% localJ %*% u)
      resultM = rbind(resultM,t(c(p1,p2,p3,var)))
    }
  }
}
resultM
maxVar = max(resultM[,4])
deff = 3
merr = 0.05
zalpha=1.96
numSamples = maxVar*deff*zalpha*zalpha/(merr*merr)

# Run this lines 54-57 commented to get variance of the simple design (0,1,1).
# Then run this with the same lines uncommented to get variance of the worst-
# case design for range ([0.01-0.15, 0.1-0.5, 0-0.02]). The best design for
# for this worst case invest r=0.025141 in the pattern (0,0,1).

