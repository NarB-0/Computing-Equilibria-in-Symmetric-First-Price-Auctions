# assumes value probabilty distribution is uniform
# very hardcoded values
import math
import random

EPSILON = 0.001
MAX_ITERATIONS = 10
MAX_VALUE = 100
MAX_BID = 100
N = 2
STEP = 1

# def generate_bidding_strategy():

#     current_bidding_strategy = [0]

#     for _ in range(len(possible_bids) - 1):

#         current = random.choice(possible_values)

#         current_bidding_strategy.append(current)

#     current_bidding_strategy.sort()
#     current_bidding_strategy.append(MAX_VALUE)
#     return current_bidding_strategy

def calculate_winning_probability(bidding_strategy, possible_bids, bid):
    i = possible_bids.index(bid)

    probability_less_than = bidding_strategy[i] / MAX_VALUE
    probability_equal = (bidding_strategy[i + 1] - bidding_strategy[i]) / MAX_VALUE
    winning_probabilty =  probability_less_than + (1 / N) * probability_equal
    # winning_probabilty = probability_less_than * probability_less_than + (1 / 2) * (2) * probability_equal *probability_less_than + (1/3)* probability_equal *probability_equal 

    return winning_probabilty 


def calculate_expected_utility(winning_probabilty, value, bid):
    return winning_probabilty * ( value - bid)

def compute_new_strategy(best_bids, possible_bids):
    new_strategy = []
    for bid in possible_bids:
        # Find the first value whose best bid is
        # at least this bid
        for value, best_bid in zip(possible_values,best_bids):
            if best_bid >= bid:
                new_strategy.append(value)
                break
        else:
            # Bid is never reached
            new_strategy.append(MAX_VALUE)

    new_strategy.append(MAX_VALUE)
    return new_strategy

def get_bid_from_strategy(strategy, value):

    for i in range(len(possible_bids)):

        if strategy[i] <= value < strategy[i + 1]:

            return possible_bids[i]

    # At the maximum value, use the last different interval.

    for i in range(len(possible_bids) - 1, -1, -1):

        if strategy[i] < strategy[i + 1]:

            return possible_bids[i]

    raise ValueError("Strategy has no nonempty intervals")

def calculate_deviation(best_utilities, old_strategy):


    # Best utilitites passed in determines the utlitites U for game =  (B', B , B, B ,... , B) 
    # so the best utilitues is actually the utlities of player playing best strategy B' again others plauing B

    # We want to find how much of a utility gain we get
    # with the new strategy aginast old strategies  
    # compared to the old strategy agians old strategies

    old_utilities = []
    chosen_bids = []
    for value in possible_values: 
        chosen_bid = get_bid_from_strategy(old_strategy, value)
        winning_probability = calculate_winning_probability(old_strategy, possible_bids, chosen_bid)
        chosen_bids.append(chosen_bid) 
        expected_utility = calculate_expected_utility(winning_probability , value, chosen_bid) 
        old_utilities.append(expected_utility)

    deviations = [max(0, best - old) for best, old in zip(best_utilities, old_utilities)]
    print("chosen bids" + str(chosen_bids) + "\n")
    print("old_utilities" + str(old_utilities) + "\n")
    print("deviations" + str(deviations) + "\n")

    return max(deviations)


def make_clean(bidding_strategy, possible_bids):
    result = "Bidding function = {\n"
    for i, bid in enumerate(possible_bids):
        # Skip bids that are never used
        if bidding_strategy[i] == bidding_strategy[i + 1]:
            continue

        if i == len(possible_bids) - 1:
            result += (f"{bid} if {bidding_strategy[i]} <= value <= {bidding_strategy[i + 1]}\n")
        else:
            result += (f"{bid} if {bidding_strategy[i]} <= value < {bidding_strategy[i + 1]}\n"
            )
    result += "}"

    return result


# bidding_strategy = [0, 0, 0, 0, 0, 0, 0]
# possible_bids = [0, 25, 50, 75, 100]

# goes up from 0 to exactly MAX_BID in steps of step 
possible_bids = [num for num in range(0, (MAX_BID )+1 , STEP)]
possible_values = [i/100 for i in range(0,(MAX_VALUE*100 )+1)]

# bidding_strategy represents (alpha) the vector of thresholds
bidding_strategy = [value for value in possible_bids]
# bidding_strategy = generate_bidding_strategy()

bidding_strategy.append(MAX_BID)
print(" Possible Bids : " + str(possible_bids))
print("\n Possible Values : " + str(possible_values))
print("\n Initaial Bidding Strategy : " + str(bidding_strategy))

# how much error there is 
deviation = float(math.inf)

# number of iterations done
iteration = 0

# seen strategies
seen_strategies = {}
print(" -------------------------------------------------------------------------------------------- " )
print("Starting Loop")
print(" -------------------------------------------------------------------------------------------- " )

while iteration < MAX_ITERATIONS :

    # Detect loop early
    strategy_tuple = tuple(bidding_strategy)
    if strategy_tuple in seen_strategies:
        print(f"LOOP FOUND: strategy at iteration {iteration} was already seen at iteration {seen_strategies[strategy_tuple]}")
        break

    seen_strategies[strategy_tuple] = iteration

    best_bids = []
    best_utilities = []

    new_strategy = []
    current_bid_index = 0
    for value in possible_values:
        best_bid = 0
        best_utility = float("-inf")
        for bid in possible_bids:
            winning_probabilty = calculate_winning_probability(bidding_strategy, possible_bids, bid)
            expected_utility = (calculate_expected_utility(winning_probabilty, value, bid))       

            if expected_utility  > best_utility :
                best_bid = bid
                best_utility = expected_utility
    
        # save best bid for each value in best_bids array
        best_bids.append(best_bid)
        best_utilities.append(best_utility)
        print((value,best_bid ,best_utility)) 
    # print(sum(best_utilities)/len(best_utilities))

    new_strategy = compute_new_strategy(best_bids, possible_bids)
    deviation = calculate_deviation(best_utilities, bidding_strategy )
    print(str(bidding_strategy )+ "\n")

    print(str(deviation) + "\n")

    if deviation <= EPSILON : 
        print("Approximate equilibrium found")
        break
    bidding_strategy = new_strategy  
    iteration +=1  


print(make_clean(bidding_strategy, possible_bids))
