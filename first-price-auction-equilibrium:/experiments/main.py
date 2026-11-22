import random
from efficient_method import efficient_e_equilibrium
from cdfCreator import create_random_2_piecewise_cdf, create_2_piecewise_cdf, create_uniform_cdf

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
                
    def random_cdf_equidistant_bids():
        bidding_space = [i/100 for i in range(100)]
        print()

        # experiment try 1000 times create a random cdf and use it to find the equilibrium 
        # and find the number of times we have bid skipping
        no_bid_skipping = 0
        bid_skipping = 0
        for i in range(1000):
            strategy =  efficient_e_equilibrium(4, 2, bidding_space , create_random_2_piecewise_cdf)
            if check_bid_skipping(strategy):
                # print(make_clean(strategy,bidding_space ))
                bid_skipping += 1
            else:
                no_bid_skipping +=1

            if i % 100 == 99:
                print(str(i+1) + " checked")
        print("Number of strategies where bids were skipped : " + str(bid_skipping))

    def generate_random_bidding_space():
        # 5 bids other than 0
        n = 5
        # Generate random, non-equidistant bids
        bidding_space = [0] + sorted(random.sample([i / 100 for i in range(1, 100)], n))    
         
        return bidding_space

    def random_bidspace_uniform_cdf():
        # changfe this so that the bidding space is not equidistant
        bidding_space = generate_random_bidding_space()
        print()

        # experiment try 100 times create a random bidding space
        # with uniform cdf and use it to find the equilibrium 
        # and find the number of times we have bid skipping
        no_bid_skipping = 0
        bid_skipping = 0
        for i in range(100):
            bidding_space = generate_random_bidding_space()

            strategy =  efficient_e_equilibrium(4, 2, bidding_space , create_uniform_cdf)
            if check_bid_skipping(strategy):
                print(bidding_space)
                print(make_clean(strategy,bidding_space ))
                bid_skipping += 1
            else:
                no_bid_skipping +=1

            if i % 10 == 9:
                print(str(i+1) + " checked")
        print("Number of strategies where bids were skipped : " + str(bid_skipping))

    bidding_space = [0, 0.11, 0.25, 0.33, 0.48, 0.7]
    strategy =  efficient_e_equilibrium(4, 2, bidding_space , create_uniform_cdf)
    print(bidding_space)
    print(make_clean(strategy,bidding_space ))

    bidding_space = [0, 0.11, 0.25, 0.33, 0.7]
    strategy =  efficient_e_equilibrium(4, 2, bidding_space , create_uniform_cdf)
    print(bidding_space)
    print(make_clean(strategy,bidding_space ))
