# scoring functions 

# https://en.wikipedia.org/wiki/Scoring_rule

import numpy as np
# log: ln r 

# take ln of probability 
def ln_score(r):
    return(np.log(r)) 



# quadratic / Brier
# 2r_i - sum r_j^2 
def quad_score(i, r): # r_i probability assigned to correct answer , C is # classes
    r_hat_i = r[-i]
    ri = r[i] 
    r2 = np.square(r_hat_i)
    qs = 2*ri - np.sum(r2)
    return(qs)
    
# spherical scoring rule
def sphere_score(i, r): # r is the array of all values
    sqsum =0
    ri = r[i]
    for el in r:
        sqsum=sqsum+np.pow(el, 2)
    den = np.sqrt(sqsum)
    return( float(ri/den))
    
