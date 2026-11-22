import math
import numpy

from computeStrategy import computeStrategy

def get_min_difference(bidding_space):
    # assume that bidding space will at least have 2 items

    min_diff = math.inf
    prev = bidding_space[0]
    
    for bid in (bidding_space[1:]):
        diff = bid - prev
        min_diff = min(min_diff, diff)
        prev = bid

    return min_diff

def calculate_delta(epsilon, alpha, n, m , L):
    return (((epsilon) ** (5 * n)  * (alpha) ** (3 * n ))  / (100 * (n)**(3) * (L)**(4)))**m

def efficient_e_equilibrium (epsilon, n, bidding_space, cdf_creator):
    # Input: 𝜀 > 0, 𝑛, bids 𝐵 = {𝑏1, . . . , 𝑏𝑚}, 𝐿-Lipschitz and 𝜀-strongly increasing cdf 𝐹
    # Output: Strategy profile 𝒔 = (𝑠0, . . . , 𝑠𝑚) constituting a symmetric 𝜀-BNE


    strategy = []   
    #maybe start with not making the function delta strongly increasing 

    # this is the minimum difference between two consecutive bids in the bidding space
    alpha = get_min_difference(bidding_space)

    m = len(bidding_space)

    # Lipschitz constant of the cdf function 
    # this will be the max height of the piecewise pdf if i do that method 
    # for uniform == 1
    cdf_F, L = cdf_creator()

    # delta = calculate_delta(epsilon, alpha, n, m , L)
    # use a precomputed delta because when m is largedelta is non existent
    delta = 0.0000000001
    # print(delta)
    
    left_utility = 0 
    right_utility = 1

    strategy = computeStrategy(right_utility, delta, n, bidding_space, cdf_F)
    while abs(right_utility   - left_utility) > delta:
        canditate_utility = (right_utility + left_utility)/2 

        new_strategy = computeStrategy(canditate_utility, delta, n, bidding_space, cdf_F)
        first_jump_point = new_strategy[0]
        if first_jump_point == 0 :
            left_utility = canditate_utility
        else:
            right_utility = canditate_utility
            strategy = new_strategy
    strategy[0] = 0
    return strategy
