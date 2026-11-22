import math
import numpy

from computeStrategy import computeStrategy
from cdfCreator import create_random_2_piecewise_cdf, create_2_piecewise_cdf, create_uniform_cdf

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

if __name__ == "__main__":

    def make_clean(bidding_strategy, bidding_space):
        result = "Bidding function = {\n"
        for i, bid in enumerate(bidding_space):
            # Skip bids that are never used
            if bidding_strategy[i] == bidding_strategy[i + 1]:
                continue

            if i == len(bidding_space) - 1:
                result += (f"{bid} if {bidding_strategy[i]} <= value <= {bidding_strategy[i + 1]}\n")
            else:
                result += (f"{bid} if {bidding_strategy[i]} <= value < {bidding_strategy[i + 1]}\n"
                )
        result += "}"

        return result

    def check_bid_skipping(strategy):
        # if the number at posiiton i == to the numner at ostition at i+1 
        # it means that there is bid skippinh
        # what we want to check if if there is a equilibrium strategy 
        # such that a bid is skippd before a threshold is reached so once a bid is sckipped a bid 
        # after is also used 

        prev = strategy[0]
        bid_skipping = False
        for threshold in strategy[1:]:
            if threshold - prev <= 0.0000000001 and not bid_skipping : 
                # first bid skipping found
                bid_skipping = True
            elif threshold-prev > 0.0000000001 and bid_skipping:
                # a bid skipping happened and you found the another bid that got used
                return True 
            else:
                prev = threshold
            
        return False
                

    bidding_space = [i/100 for i in range(100)]
    print()

    strategy =  efficient_e_equilibrium(4, 2, bidding_space , create_random_2_piecewise_cdf)
    print(make_clean(strategy,bidding_space ))


    # experiment try 1000 times create a random cdf and use it to find the equilibrium 
    # and find the number of times we have bid skipping
    no_bid_skipping = 0
    bid_skipping = 0
    for i in range(1000):
        strategy =  efficient_e_equilibrium(4, 2, bidding_space , create_random_2_piecewise_cdf)
        if check_bid_skipping(strategy):
            print(make_clean(strategy,bidding_space ))
            bid_skipping += 1
            break
        else:
            no_bid_skipping +=1

        if i % 100 == 0:
            print(i)
    print("Number of strategies where bids were skipped : " + str(bid_skipping))
