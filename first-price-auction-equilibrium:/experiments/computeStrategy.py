import math

def computeStrategy(canditate_utility, delta, n, bidding_space, cdf_F):
    # Input: 𝑈 ∈ [0, 1], 𝛿 > 0
    # Output: A vector 𝒔 = (𝑠0, . . . , 𝑠𝑚) with 0 ≤ 𝑠0 ≤ · · · ≤ 𝑠𝑚 = 1

    strategy = [0 for i in range(len(bidding_space)+1)]
    utilities = [0 for i in range(len(bidding_space)+1)]

    # last_jump_point = 1
    # last_jump_point_utility = canditate_utility
    strategy[-1] = 1
    utilities[-1] = canditate_utility

    # need to look into this because we have bidding space array which goes from b1 to bm 
    # in my implementation it goes from b0 to bm-1
    # to keep consistent ill create bj to bm which will make it more cleaner 
    # but we have strategy array which goes from s0 to sm
    # let i = i for S and let j be i-1 

    for i in range(len(bidding_space) , 0 , -1):
        j = i-1
        if (strategy[i] - bidding_space[j] ) * computation_delta(strategy[i], strategy[i] , cdf_F, n) <= utilities[i] :
            # S (i-1) needs to be skipped
            strategy[i-1] = strategy[i]
            utilities[i-1] = utilities[i]
        elif (strategy[i] - bidding_space[j]) * computation_delta(bidding_space[j], strategy[i], cdf_F, n) >= utilities[i]:
            strategy[i-1] = bidding_space[j]
            utilities[i-1] = 0 
        else:
            # binary search to find 𝑠𝑖−1 ∈ (𝑏𝑖, 𝑠𝑖)
            # | (𝑠𝑖 − 𝑏𝑖)Δ(𝑠𝑖−1, 𝑠𝑖) − 𝑈𝑖| ≤ delta
            strategy[i-1] =  binarysearch(bidding_space[j], strategy[i], cdf_F, n , delta, utilities[i] )
            utilities[i-1] = (strategy[i-1] - bidding_space[j] ) * computation_delta(strategy[i-1], strategy[i], cdf_F, n)
    return strategy

def computation_delta(x, y, cdf_F, n):
    total = 0 
    x = cdf_F(x)
    y = cdf_F(y)
    for i in range(n):
        total +=  (x ** (n-1-i)) * (y ** i)

    return 1/n * total 

def binarysearch(l,r, cdf_F, n , delta, Ui):
    left = l
    right = r
    while  (right - left) > delta :
        mid =  (left + right ) / 2
        current_utlity = (r - l ) * computation_delta(mid, r, cdf_F, n)
        if  abs(current_utlity - Ui) <= delta:
            return mid
        elif current_utlity < Ui :
            left = mid
        else:
            right = mid

    return (left + right) / 2