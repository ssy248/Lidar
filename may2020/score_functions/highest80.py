# highest of 80 percent freq.

def highest80(fromi):
    highest =[0] # now it is array
    indexhighest = [-1] # now it is array
    (px, py) = dlookupdict[fromi]
    for j in range(-10, 11):
        jx = px+j
        if jx>xmax-1 or jx<xmin: # check if pts in range
            continue
        for k in range(-10, 11):
            jy = py+k
            # check if pts are in range
            if jy>ymax-1 or jy<ymin:
                continue
            toi = dinvlookupdict[(jx, jy)]
            t = dtrajcount[(fromi, toi)]
            #if t>0:
                #print(t)
            hi = np.max(highest)
            if t > 0.8*hi: # instead of checking if it is > highest, check if >= 0.8*highest, prune those less
                highest.append(t)
                indexhighest.append(toi)
    # remove the indices that are too low
    ind=0
    nhighest=[]
    nindexhighest=[]
    m = np.max(highest)
    for val in highest:
        if val >= float(0.8*(m)):
            nhighest.append(val)
            nindexhighest.append(indexhighest[ind])
        ind=ind+1
    return nhighest, nindexhighest
    
