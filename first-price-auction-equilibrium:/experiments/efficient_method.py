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
        print(canditate_utility)

        new_strategy = computeStrategy(canditate_utility, delta, n, bidding_space, cdf_F)
        first_jump_point = new_strategy[0]
        if first_jump_point == 0 :
            left_utility = canditate_utility
        else:
            right_utility = canditate_utility
            strategy = new_strategy
        print(strategy)
    return strategy

if __name__ == "__main__":
    def cdf(x):
        return x
    
    print(efficient_e_equilibrium(0.00001, 2, [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9, 1], cdf))
