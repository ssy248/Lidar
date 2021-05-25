# plot 
# the frequency grid 
# march 26 2021

# replace  with other score function , and 80 percent highest

# december highest 
# step 4 b 
fromi = 107010

scores=[]
inds = []

highest = 0
indexhighest = fromi
(px, py) = dlookupdict[fromi]

print("x is", px)
print("y is", py)

# check max index
imax = fromi
maxval = 0

firstrow = 0
firstrowel =0
datamatrix = []
datamatrix2 = []
datarow =[]
datarow2 = []
for j in range(-10, 11):
    jy = py+j
    
    datarow=[]
    if jy>ymax-1 or jy<ymin: # check if pts in range
        continue
    for k in range(-10, 11):
        jx = px+k
        # check if pts are in range
        if jx>xmax-1 or jx<xmin:
            continue
        toi = dinvlookupdict[(jx, jy)]
        t = dtrajcount[(fromi, toi)]
        if j==0 and k==0:
            t = -10
        # save t value
        datarow.append(t)
        scores.append(t)
        inds.append(toi)
        
        if t>maxval:
            maxval=t
            imax = toi
        
    # end of current row
    if firstrow==0:
        firstrow=1
        datamatrix = datarow
        continue
    datamatrix = np.vstack((datamatrix, datarow))
    
 #calculate score:

# build datamatrix2 
hi = np.max(scores)
ind=0

trans_scores=[]

firstrow=0

for s in scores:
    s1 = quad_score(ind,scores)
    
    trans_scores.append(s1)
    ind=ind+1
    
# use reshape matrix
datamatrix2 = np.reshape(trans_scores, (21,21))
