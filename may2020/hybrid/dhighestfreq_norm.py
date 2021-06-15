# normalized dhighest (mean , std dev)

def dhighestfreq_norm(fromi):
    highest = 0
    indexhighest = fromi
    (px, py) = dlookupdict[fromi]
    scores = []
    inds = []
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
            scores.append(t)
            inds.append(toi)
            #if t>0:
                #print(t)
            if t > highest:
                highest=t
                indexhighest=toi
                
    sd= statistics.stdev(scores)
    mu = np.mean(scores)
    # remove indices that are too low
    nhighest=[]
    nindex = []
    ind1 = 0
    for val in scores:
        # transformed 
        val_n = (val - mu)/sd
        if val_n >= 0.8: #float(0.8*(hi)):
            nhighest.append(val_n)
            nindex.append(inds[ind1])
        ind1 = ind1+1
    return nhighest, nindex

    
