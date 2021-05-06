# use the frequency scores to be added

# hybrid score function April 30 complete procedure

totalcomparisons = 0

c1 = 1
c2 = 12

# new params
totresults = []
totclusterids=[]

#diff. category of accuracy index
missedmatching = 0
wrongmatching =0 # matched to a different cluster
continuedmatching = 0 # continues erroneously 

clustering_error = 0 

#####
initialframe = 410
endframe = 500

unew = map10[initialframe]

ca = list(range(c1, c2+1))
#unew = [1]
carray = np.setdiff1d(ca, unew)

print("carray :", carray)

for initialcluster in ca:#range(c1, c2+1):
    
    
    arrayx = []
    arrayy = []
    pavex = []
    pavey = []

    phx = [] # previous high x values
    phy =[] 


    obnum = 1

    totalmap ={}
    totalmapscore={}

    prevmap = {}
    # may 3 2021
    prevmapscore={}

    mf = defaultdict(list)
    # maximum object/cluster id in any frame
    mx = 20

    for j in range(0, mx):
        mf[j]=0 

    matchfreq= mf
    
    # April 30
    # array for counts of pts in clusters
    counts = {} #[]
    # normalized matchfreq scores
    normalmatchfreq = mf

    thres= 10

    finalarray=[]

    finalarray.append(initialcluster)

    finalx =[]
    finaly =[]

    avex =[]
    avey =[]

    xvalues =[]
    yvalues =[]

    # edited method
    angles = []
    
    for i in range(initialframe, endframe+1):
        name = "file_out"
        name = name+str(i)
        name = name+".csv"
        firstrow=0
        # clear matchfreq
        for j in range(0, mx):
            matchfreq[j] =0
            normalmatchfreq[j]=0

        currentmap3 = {} # average coordinates

        print("curr frame is:", i)


        with open(name) as csv_file:
            f =0 
            # reset hxvalues , hyvalues
            hxvalues = []
            hyvalues=[]

            obnum=1 

            currentmap= {}
            currentmapscore={} # may 3 2021 

            csv_reader = csv.reader(csv_file, delimiter=",")

            if i==initialframe:
                for row in csv_reader:
                    # no need for first row skip 
                    clusterid = float(row[0])
                    if clusterid==initialcluster:
                        xpoint = float(row[1])
                        ypoint = float(row[2])
                        #print("xpt", xpoint)
                        #print("ypt", ypoint)
                        arrayx.append(xpoint)
                        arrayy.append(ypoint)
                        xr = round(xpoint)
                        yr = round(ypoint)
                        fromi = dinvlookupdict[(xr,yr)]
                        hlist, ilist = highest80(fromi)
                        #ilist = np.unique(i1)
                        hind = 0
                        for ind1 in ilist:
                            prevmap[ind1] = 1
                            prevmapscore[ind1] = hlist[hind]
                            hind=hind+1
                        #i1 = newhighestfreq(fromi)
                        #prevmap[i1] = 1

                plt.scatter(arrayx, arrayy)

                avx = np.mean(arrayx)
                avy = np.mean(arrayy)

                finalx.append(avx)
                finaly.append(avy)

                # save angle

                plt.annotate(i, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')

                #append avx and avy
                avex.append(avx)
                avey.append(avy)

                # reset ky 
                ky = initialcluster
                continue
            # counter of number of points in cluster: unique points?
            ccount = 1
            for row in csv_reader:
                clusterid = float(row[0])

                if clusterid != obnum:
                    numo1 = float(obnum)
                    # append into dictionary of maps
                    totalmap[numo1] = currentmap
                    totalmapscore[numo1] = currentmapscore # May 3 2021 
                    
                    counts[numo1] = ccount
                    normalmatchfreq[numo1] = matchfreq[numo1]/ccount
                    
                    if normalmatchfreq[numo1] > f:#matchfreq[numo1] > f:
                        f = normalmatchfreq[numo1] #matchfreq[numo1]
                        print("f is", f)
                        ky = numo1

                        hxvalues = xvalues
                        hyvalues = yvalues
                    obnum= clusterid
                    currentmap={}
                    currentmapscore={}
                    # take the average
                    avecurrentx = np.mean(xvalues)
                    avecurrenty = np.mean(yvalues)
                    currentmap3[numo1] = [avecurrentx, avecurrenty]

                    xvalues =[]
                    yvalues =[]
                    
                    ccount=1
                    continue

                xpoint = float(row[1])
                ypoint = float(row[2])
                xr = round(xpoint)
                yr = round(ypoint)
                ccount=ccount+1
                
                xvalues.append(xpoint) # save to array 
                yvalues.append(ypoint)
                fromi = dinvlookupdict[(xr,yr)]
                # function to find highest freq 
                h1, i1 = highest80(fromi)
                # save to map
                #currentmap[i1] = 1
                hind=0
                for ind1 in i1:
                    currentmap[ind1] = 1
                    currentmapscore[ind1] = h1[hind]
                    hind=hind+1
                # check prev map
                val = prevmap.get(fromi)
                hval = prevmapscore.get(fromi) # May 3 2021
                if val == None:
                    pass
                else:
                    numo = float(obnum)
                    print("hval is", hval)
                    #print("hval type is,", type())
                    matchfreq[numo] = matchfreq[numo]+ float(hval) # 1 to hval 
            # check at end of file
            numo2 = float(clusterid)
            counts[numo2] = ccount
            normalmatchfreq[numo2] = matchfreq[numo2]/ccount
            
            avecurrentx = np.mean(xvalues) ##USE AS CURRENT X
            avecurrenty = np.mean(yvalues)
            currentmap3[numo2] = [avecurrentx, avecurrenty]
            totalmap[numo2] = currentmap
            
            if normalmatchfreq[numo2] > f:
                ky = numo2
                hxvalues = xvalues
                hyvalues = yvalues
                totalmap[ky]= currentmap

            if len(hxvalues) ==0:
                foundmin=0
                mindist = thres
                c_first=0
                for c in currentmap3:
                    cvalue = currentmap3[c]
                    cx = cvalue[0]
                    cy = cvalue[1]
                    ax = finalx[-1]
                    ay = finaly[-1]
                    dist1 = pow(cx - ax,2) + pow(cy - ay,2)
                    dist = math.sqrt(dist1)
                    if dist < thres:
                        if c_first==0:
                            c_first=1
                            minclust=c
                            mcx = cx
                            mcy= cy
                            mindist = dist
                        foundmin=1
                        if dist< mindist:
                            mindist = dist
                            minclust=c
                            mcx = cx
                            mcy = cy
                if foundmin==1:
                    print("found min")
                    print("dist is", mindist)
                    print("minclust is", minclust)
                    if len(angles)==0:
                        print("angles array is of length 0 and minclust:", minclust)
                        prevmap = totalmap[minclust]
                        prevmapscore = totalmapscore[minclust]
                        avx = mcx
                        avy = mcy 
                        ## move to end
                        ## finalarray.append(minclust)                       
                        # add to angles
                        xdiff = avx - finalx[-1]
                        ydiff = avy - finaly[-1]
                        ## check initial direction 2/28/21 
                        if avy >20: # +y, -x
                            # break if both directions are unsatisfied / one direction unsat.
                            if xdiff >0 and ydiff <0:
                                print("both dir. unsat.")
                                # plot
                                plt.scatter(mcx, mcy)
                                plt.annotate("wrong dir.", (mcx, mcy))
                                break
                        if avy <20: # -y, +x
                            if xdiff<0 and ydiff>0:
                                print("both dir. unsat.")
                                plt.scatter(mcx, mcy)
                                #plot 
                                plt.annotate("wrong dir.", (mcx, mcy))
                                break
                        rad = math.atan2(ydiff, xdiff)
                        ang = math.degrees(rad)
                        # moved here 
                        finalarray.append(minclust)  
                        
                        if ang<0:
                            ang = 360+ang
                        angles.append(ang)

                        finalx.append(mcx)
                        finaly.append(mcy)



                        #plt.scatter(mcx, mcy)
                        #plt.annotate(i, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')
                        continue
                    prev_avex = finalx[-1]
                    prev_avey = finaly[-1]

                    xdiff_curr = mcx - prev_avex #how is avx set?
                    ydiff_curr = mcy - prev_avey 
                    
                    if mcy >20: # +y, -x
                        # break if both directions are unsatisfied / one direction unsat.
                        if xdiff_curr >0 and ydiff_curr <0:
                            print("both dir. unsat.; angles not empty")
                            # plot
                            plt.scatter(mcx, mcy)
                            plt.annotate("wrong dir.", (mcx, mcy))
                            break
                    if mcy <20:
                        if xdiff_curr<0 and ydiff_curr>0:
                            print("both dir. unsat.; angles not empty")
                            # plot
                            plt.scatter(mcx, mcy)
                            plt.annotate("wrong dir.", (mcx, mcy))
                            break
                    
                    # calc angle
                    rad = math.atan2(ydiff_curr, xdiff_curr)

                    ang = math.degrees(rad)
                    if ang<0:
                        ang = 360+ang

                    prev_ang = angles[-1]

                    ang_diff = abs(ang - prev_ang)

                    print("prev ang :", prev_ang)
                    print("curr ang:", ang)

                    print("ang_diff is:", ang_diff)
                    if ang_diff <= 30: # change from 45 to 30
                        print("angle holds")
                        prevmap= totalmap[minclust]
                        prevmapscore = totalmapscore[minclust]
                        avx = mcx
                        avy =mcy
                        finalarray.append(minclust)
                        finalx.append(mcx)
                        finaly.append(mcy)
                        # append to slopes / diffs
                        #xdiff.append(avx - avex[-1])
                        #ydiff.append(avy - avey[-1])
                        #avex.append(avx)
                        #avey.append(avy)
                        #append to angles
                        angles.append(ang)
                    else:
                        print("angles too large, stop")
                        break
                else:
                    print("not found and end, after last frame", i)
                    break
            if len(hxvalues) !=0:
                finalarray.append(ky)
                prevmap = totalmap[ky]
                prevmapscore = totalmapscore[ky]  # add to prevmapscore May 3 2021

                avx = np.mean(hxvalues)
                avy = np.mean(hyvalues)

                prev_avx = finalx[-1]
                prev_avy = finaly[-1]

                # update angles
                xdiff = avx - prev_avx
                ydiff = avy - prev_avy 
                rad = math.atan2(ydiff, xdiff)
                ang = math.degrees(rad)
                if ang <0:
                    ang = 360+ang
                angles.append(ang)

                finalx.append(avx)
                finaly.append(avy)
            
            if i % 10==0:
                print("(map10) i is", i)
                print("(map10) key is", ky)
                m10 = map10[i]
                m10.append(ky)
                # check sim clusts
                v1 = errorclusters.get(i)
                if v1!=None:
                    errorarray= errorclusters[i]
                    for el in errorarray:
                        for e in el:
                            if e == ky:
                                m10.extend(el)
                map10[i] = m10

            #print("final x", finalx)
            #print("final y", finaly)


    print("initial cluster", initialcluster)
    print("initial frame", initialframe)

    print("final array is", finalarray)
    
    listclusterids= finalarray
    
    print("listclusterids is", listclusterids)
    
    # plot
    
    
    alen = len(finalarray)
    print("length of array ", alen)
    
    xv1=[]
    yv1=[]

    ax =[]
    ay =[]

    acounter=0
    for i in range(initialframe, initialframe+alen):
        name = "file_out"
        name = name+str(i)
        name = name+".csv"


        a = finalarray[acounter]
        xarray = []
        yarray = []
        with open(name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                clusterid = float(row[0])
                xpoint = float(row[1])
                ypoint = float(row[2])

                if clusterid == a:
                    xarray.append(xpoint)
                    yarray.append(ypoint)


            # plot
            plt.scatter(xarray,yarray)
            avx = np.mean(xarray)
            avy = np.mean(yarray)
            plt.annotate(i, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')

            ax.append(avx)
            ay.append(avy)

        acounter =acounter +1
        if acounter > alen:
            break

    plt.show()
    
    # app result
    result = []
    result.append(initialcluster)
    
    iframe = initialframe
    currentcluster = initialcluster
    t = True
    while t:
        nextres = findnextclusterapp(iframe, currentcluster)
        if str(nextres) == "nan":
            break
        if iframe >= endframe:
            break
        result.append(nextres)
        iframe = iframe+1
        currentcluster = nextres
        
    len1 = len(result) #datastore result
    len2 = len(listclusterids) # our result 

    setlen = min(len1, len2)
    od1 = {}
    od2 = {}
    booleanwrong=[]
    
    for j1 in range(0,setlen):
        nolongerwrong=0
        nolongerwrongoriginal=0
        frameno=initialframe+j1
        od1[frameno]=[result[j1]]
        od2[frameno]=[listclusterids[j1]]
        if result[j1]==listclusterids[j1]:
            nolongerwrong=1
            nolongerwrongoriginal=1
        if result[j1]!= listclusterids[j1]:
            v1 = errorclusters.get(frameno)
            if v1!=None:
                errorarray= errorclusters[frameno]
                for el in errorarray:
                    if result[j1] in el:
                        if listclusterids[j1] in el:
                            nolongerwrong=1
        if nolongerwrong!=1:
            booleanwrong.append(1) # wrong
        else:
            booleanwrong.append(0) # not wrong
            if nolongerwrongoriginal==0:
                clustering_error = clustering_error+1
    maxlen= max(len1, len2)
    last1 = result[setlen-1]
    last2 = listclusterids[setlen-1]
    
    if len1 != len2:
# iterate over setlen to max len
        for j2 in range(setlen, maxlen):
            nolongerwrong=0
            nolongerwrongoriginal = 0 
            frameno2 = initialframe+j2
            if len1 > len2:
                next2 = findnextcluster(frameno2, last2)
                if next2 == result[j2]:
                    nolongerwrong=1
                    nolongerwrongoriginal=1
                v2 = errorclusters.get(frameno2)
                if v2 != None:
                    errorarray = errorclusters[frameno2]
                    for el in errorarray:
                        if result[j2] in el:
                            if next2 in el:
                                nolongerwrong=1
                if nolongerwrong==1:
                    booleanwrong.append(0)
                    if nolongerwrongoriginal ==0:
                        clustering_error= clustering_error+1
                else:
                    booleanwrong.append(1)
                last2 = next2
            if len2 > len1:
                next2 = findnextclusterapp(frameno2, last2)
                if next2 == listclusterids[j2]:
                    nolongerwrong=1
                    nolongerwrongoriginal=1
                v2 = errorclusters.get(frameno2)
                if v2 != None:
                    errorarray = errorclusters[frameno2]
                    for el in errorarray:
                        if listclusterids[j2] in el:
                            if next2 in el:
                                nolongerwrong=1
                if nolongerwrong==1:
                    booleanwrong.append(0)
                    if nolongerwrongoriginal==0:
                        clustering_error=clustering_error+1
                else:
                    booleanwrong.append(1) # wrong
                last2 = next2
    d1 = {}
    d2 = {}
    
    for j1 in range(0, setlen):
        frameno = initialframe+j1
        # check similar clusters
        clusters1 = od1[frameno]
        clusters2 = od2[frameno]

        simclusters = errorclusters.get(frameno)
        if simclusters != None:
            simarray = errorclusters[frameno]
            # check if matches
            for el in simarray:
                if od1[frameno] in el:
                    clusters1.extend(el)
                if od2[frameno] in el:
                    clusters2.extend(el)
        d1[frameno] = clusters1
        d2[frameno] = clusters2
        
    maxlen= max(len1, len2)
    # set original clusters for up to maxlen
    for j2 in range(setlen, maxlen):
        frameno = initialframe+j2
        d1[frameno] = []
        d2[frameno] = []
        if len1>len2:
            d1[frameno]= [result[j2]]
        if len2>len1:
            d2[frameno]=[listclusterids[j2]]

    d1[initialframe+maxlen] = []
    d2[initialframe+maxlen] = []
    setlen = min(len1, len2)
    maxlen= max(len1,len2)
    
    for j in range(0, maxlen):

        frameno = initialframe+j 
        #print("j is", j)
        #print("frame num is", frameno)

        # all clusters within current frame
        clust1 = d1[frameno]
        clust2 = d2[frameno]


        # check clusters to next step
        for c1 in clust1:
            nc1 = findnextclusterapp(frameno, c1)
            if str(nc1) == "nan":
                #print("nc1 is nan")
                continue
            #print("frameno plus one", frameno+1)
            #print("nc1", nc1)
            nclust1 = d1[frameno+1]
            # only append if not already there
            if nc1 not in nclust1:
                nclust1.append(nc1)
            #nclust1.append(nc1)
            #nclust1 = np.unique(nclust1)
            d1[frameno+1] = nclust1
        for c2 in clust2:
            nc2 = findnextcluster(frameno, c2)
            if nc2 == -1:
                continue
            nclust2 = d2[frameno+1]
            if nc2 not in nclust2:
                nclust2.append(nc2)
            d2[frameno+1] = nclust2
        if booleanwrong[j]==1:
            set1 = set(clust1)
            intersect = set1.intersection(clust2)
            if len(intersect)>0:
                print("intersect")
                booleanwrong[j]=0
                clustering_error=clustering_error+1

    bindex = 1
    firstframewrong = -1
    for b in booleanwrong:
        if b == 1:
            firstframewrong = bindex
            break
        bindex= bindex+1

    if firstframewrong == -1:
        totalcomparisons= totalcomparisons+maxlen
    else:
        totalcomparisons= totalcomparisons+firstframewrong
        
    contflag = 0
    missedflag= 0
    
    # print length of array found
    print("len of listclusterids", len(listclusterids))
    
    if np.sum(booleanwrong) >0:
        if firstframewrong>len1:
            print("continuedly")
            print("array1", result) # array1 is app result
            print("array2", listclusterids)
            contflag= 1
            continuedmatching= continuedmatching+1
        if firstframewrong > len2: 
            print("missedly")
            print("array1", result)
            print("array2", listclusterids)
            missedmatching = missedmatching+1
            missedflag=1
        if contflag==0 and missedflag==0:
            print("wrongly")
            print("array1", result)
            print("array2", listclusterids)
            wrongmatching= wrongmatching+1
        
        if contflag==1 and missedflag==1:
            print("BOTH CONTINUED AND MISSED")
        
print("missed matchings:", missedmatching)
print("cont matchings:", continuedmatching)
print("wrong matchings:", wrongmatching)
print("total :", totalcomparisons)
print("clust. errors:", clustering_error)
