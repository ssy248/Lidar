# highest 80 with normalization added in

def highest80_quad_norm(fromi):
    scores=[]
    inds = []

    highest = 0
    indexhighest = fromi
    (px, py) = dlookupdict[fromi]


    # check max index
    imax = fromi
    maxval = 0

    for j in range(-10, 11):
        jy = py+j

        if jy>ymax-1 or jy<ymin: # check if pts in range
            continue
        for k in range(-10, 11):
            jx = px+k
            # check if pts are in range
            if jx>xmax-1 or jx<xmin:
                continue
            toi = dinvlookupdict[(jx, jy)]
            t = dtrajcount[(fromi, toi)]

            scores.append(t)
            inds.append(toi)

     #calculate score:

    hi = np.max(scores)
    ind=0

    trans_scores=[]

    #z_scores = []
    #sd = statistics.stdev(scores)
    #mu = np.mean(scores)


    for s in scores:
        s1 = quad_score(ind,scores)
        trans_scores.append(s1)
        #z = (s - mu)/sd
        #z_scores.append(z)
        ind=ind+1
    
    sd_q= statistics.stdev(trans_scores)
    mu_q = np.mean(trans_scores)
    

    # remove indices that are too low

    nhighest=[]
    nindex = []
    ind1 = 0
    for val in trans_scores:
        # transformed 
        val_q = (val - mu_q)/sd_q
        if val_q >= 0.8: #float(0.8*(hi)):
            nhighest.append(val_q)
            nindex.append(inds[ind1])
        ind1 = ind1+1

    return nhighest, nindex
