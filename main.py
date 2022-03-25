import argparse
from optimization.yin_yang import *

default_method = 'local'
default_budget = 10000
default_rtpcr_cost = 0.1
default_rat_cost = 0.03
default_igg_cost = 0.05

parser = argparse.ArgumentParser()
parser.add_argument('-C', help="Total budget available, C (in units of thousand rupees)", default=default_budget )
parser.add_argument('-cRAT', help="Cost for one RAT test(in units of thousand rupees)", default=default_rat_cost)
parser.add_argument('-cRTPCR', help="Cost for one RT-PCR test(in units of thousand rupees)", default=default_rtpcr_cost)
parser.add_argument('-cIGG', help="Cost for one IGG test(in units of thousand rupees)", default=default_igg_cost)
parser.add_argument("-m", help="select method to opimize, by default 'local optimization' is enabled, for exhaustive search, set -m grid", default=default_method)
args = parser.parse_args()

C = float(args.C)
cRAT = float(args.cRAT)
cRTPCR = float(args.cRTPCR)
cIgG = float(args.cIGG)
methods = args.m


if __name__ == '__main__':
    p_initial = [0.125,0.2,0.3]
    yin_yang_descent(cRAT, cRTPCR, cIgG, p1_start=p_initial[0], p2_start=p_initial[1], p3_start=p_initial[2])
    

