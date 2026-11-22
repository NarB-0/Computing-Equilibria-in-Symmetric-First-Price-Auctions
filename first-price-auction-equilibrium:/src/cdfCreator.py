# returns the uniform cdf and the lipschitz constant of it 
import numpy 

def create_uniform_cdf():

    def uniform_cdf(x):
        return x 

    return uniform_cdf , 1

# Creates a random 2 piecewise pdf and returns the
# cdf associated with it and the lipschitz constant of the cdf 
def create_random_2_piecewise_cdf():
    # Make a random pdf 
    # 2- piecewise constant pdf
    # - Choose a random x between 0 and 1 
    # - Choose another random h1 between 0 and 1 
    # - Choose another random h2 between 0 and 1 
    # - Normalise the h1 and h2 so area under graph is 1 
    # - To get L of the function - return max (h1, h2)

    x1 = numpy.random.uniform(0, 1)
    h1 = numpy.random.uniform(0, 1)
    h2 = numpy.random.uniform(0, 1)
    area = (x1 * h1 ) +  ((1-x1) * h2)
    h1 = h1 / area
    h2 = h2 / area

    L = max(h1, h2)

    def two_piecewise_cdf(x):
    # find area under graph for point <= x
        if x <= x1:
            return x * h1
        return (x1 * h1) + ((x - x1) * h2)

    return two_piecewise_cdf, L


def create_2_piecewise_cdf():
    # Make a random pdf 
    # 2- piecewise constant pdf
    # - Choose a random x between 0 and 1 
    # - Choose another random h1 between 0 and 1 
    # - Choose another random h2 between 0 and 1 
    # - Normalise the h1 and h2 so area under graph is 1 
    # - To get L of the function - return max (h1, h2)

    x1 = 0.5
    h1 = 100
    h2 = 0.9
    area = (x1 * h1 ) +  ((1-x1) * h2)
    h1 = h1 / area
    h2 = h2 / area

    L = max(h1, h2)

    def two_piecewise_cdf(x):
    # find area under graph for point <= x
        if x <= x1:
            return x * h1
        return (x1 * h1) + ((x - x1) * h2)

    return two_piecewise_cdf, L
