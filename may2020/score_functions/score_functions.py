# scoring functions 
import numpy as np
# log: ln r 

# take ln of probability 
def ln_score(r):
    return(np.log(r)) 



# quadratic / Brier
# 2r_i - sum r_j^2 
def quad_score(ri, r): # r_i probability assigned to correct answer , C is # classes
    qs = 2*ri - np.sum(r)
    return(qs)
    
# spherical scoring rule
def sphere_score(ri, r): # r is the array of all values
    sqsum =0
    for el in r:
        sqsum=sqsum+np.pow(el, 2)
    den = np.sqrt(sqsum)
    return( float(ri/den))
