from computeStrategy import computeStrategy


def efficient_e_equilibrium (epsilon, n, bidding_space, cdf_F):
    # Input: 𝜀 > 0, 𝑛, bids 𝐵 = {𝑏1, . . . , 𝑏𝑚}, 𝐿-Lipschitz and 𝜀-strongly increasing cdf 𝐹
    # Output: Strategy profile 𝒔 = (𝑠0, . . . , 𝑠𝑚) constituting a symmetric 𝜀-BNE


    strategy = []   
    #maybe start with not making the function delta strongly increasing 
    delta = epsilon
    
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
    def cdf(x):
        return x

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

    
    bidding_space = [0,0.2,0.4,0.6,0.8, 1]
    strategy =  efficient_e_equilibrium(0.0000000001, 3, bidding_space , cdf)
    print(make_clean(strategy,bidding_space ))
