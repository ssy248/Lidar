## June 23: 0.2, 0.3, 0.5 maps add
# Only 0.2 seconds so far

# Complete from correct version 
# june 16 add saving arrays

arrayx_map = {}
arrayy_map = {}


initialframe=400
endframe=590

c1= 1
c2= 6
# June 16 add map5 :
#unew = map5[initialframe]

#ca = list(range(c1, c2+1))
#carray = np.setdiff1d(ca, unew)

for initialcluster in range(c1, c2+1):    
    
    xarr =[]
    yarr= []  
    arrayx = []
    arrayy = []
    pavex = []
    pavey = []

    phx = [] # previous high x values
    phy =[] 


    obnum = 1

    totalmap ={}
    prevmap = {}
    prevmapscore={}
    poolmap ={} # pooling
    prevpoolmap = {}

    mf = defaultdict(list)
    # maximum object/cluster id in any frame
    mx = 20

    for j in range(0, mx):
        mf[j]=0 

    matchfreq= mf


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

    rvals=[]
    
    # June 21 variable
    goforward=0
    nogoforward=0

    for i in range(initialframe, endframe+1):
        name = "file_out/file_out"
        name = name+str(i)
        name = name+".csv"
        firstrow=0
        # clear matchfreq
        for j in range(0, mx):
            matchfreq[j] =0

        # reset xvalues and yvalues, May 18
        xvalues=[]
        yvalues=[]

        currentmap3 = {} # average coordinates

        print("curr frame is:", i)


        with open(name) as csv_file:
            f =0 
            # reset hxvalues , hyvalues
            hxvalues = []
            hyvalues=[]

            obnum=1 

            currentmap= {}
            currentmapscore={}

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
                        #h1, i1 = highest80_sphere(fromi)
                        h1, i1 = dhighestfreq(fromi)
                        #h1, i1 = highest80_quad_norm(fromi) # May 26 # highest80_quad_norm or highest80_quad
                        # save to map
                        prevmap[i1] = h1
                        """hind=0
                        for ind1 in i1:
                            prevmap[ind1] = 1
                            prevmapscore[ind1] = h1[hind]
                            hind=hind+1"""
                        # pooling
                        """pv = poolmap.get(i1)
                        if i1==None:
                            # set count as 1 
                            poolmap[i1]=1
                        else:
                            pc=float(pv)
                            poolmap[i1] = pc+1"""

                        #prevmap[i1] = 1

                plt.scatter(arrayx, arrayy)

                avx = np.mean(arrayx)
                avy = np.mean(arrayy)

                finalx.append(avx)
                finaly.append(avy)
                
                prevpoolmap = poolmap
                poolmap= {} # reset

                # save angle

                plt.annotate(i, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')

                #append avx and avy
                avex.append(avx)
                avey.append(avy)

                # reset ky 
                ky = initialcluster
                continue
            for row in csv_reader:
                clusterid = float(row[0])

                if clusterid != obnum:
                    numo1 = float(obnum)
                    # append into dictionary of maps
                    totalmap[numo1] = currentmap
                    if matchfreq[numo1] > f:
                        f = matchfreq[numo1]
                        print("f is", f)
                        ky = numo1

                        hxvalues = xvalues
                        hyvalues = yvalues
                        hrvals = rvals

                    obnum= clusterid
                    currentmap={}
                    currentmapscore={}
                    # take the average
                    avecurrentx = np.mean(xvalues)
                    avecurrenty = np.mean(yvalues)
                    currentmap3[numo1] = [avecurrentx, avecurrenty]

                    xvalues =[]
                    yvalues =[]
                    rvals = []

                    continue

                xpoint = float(row[1])
                ypoint = float(row[2])
                xr = round(xpoint)
                yr = round(ypoint)
                

                if (xr, yr) not in rvals:
                    rvals.append((xr, yr))
                    rvalindex= i

                xvalues.append(xpoint) # save to array 
                yvalues.append(ypoint)
                fromi = dinvlookupdict[(xr,yr)]
                
                # June 22
                if goforward >0:
                    # check
                    if goforward==1: # trajcount2
                        # fromi is the previous fromi
                        toi_current = fromi 
                        
                        # look from prevmap
                        for f in fromlist:
                            hi_index = highestfreq2(fromi)
                            
                            (hx, hy) = dlookupdict[hi_index]
                            
                            if hx == xr and hy == yr:
                                # increment
                                print(" 0.2 sec next found")
                                
                                numo = float(obnum)
                                matchfreq[numo] = matchfreq[numo]+1
                                # check: break statement?
                                break
                                
                            #currentmap[hi_index] = 1 # or look up the value
                        
                        continue
                    
                    if goforward==2: # trajcount3
                        hi_index= highestfreq3(fromi)
                    
                    if goforward==3: # trajcount5
                        hi_index = highestfreq5(fromi)
                else:
                
                    # function to find highest freq 
                    #h1, i1 = highest80_sphere(fromi)
                    h1, i1 = dhighestfreq(fromi)
                    #h1, i1 = highest80_quad_norm(fromi)  # highest80_quad_norm or highest80_quad
                    currentmap[i1] = h1
                
                    # pooling
                    """pv = poolmap.get(i1)
                    if i1==None:
                        # set count as 1 
                        poolmap[i1]=1
                    else:
                        pc=float(pv)
                        poolmap[i1] = pc+1"""
                
                    # save to map
                    """hind=0
                    for ind1 in i1:
                        currentmap[ind1]=1
                        currentmapscore[ind1] = h1[hind]
                        hind=hind+1"""
                    # check prev map
                    val = prevmap.get(fromi)
                    # pool : poolmap
                    poolval = prevpoolmap.get(fromi) # June 16
                    # set the weights 
                    if val == None:
                        pass
                    else:
                        numo = float(obnum)
                        matchfreq[numo] = matchfreq[numo]+1
            numo2 = float(clusterid)
            avecurrentx = np.mean(xvalues) ##USE AS CURRENT X
            avecurrenty = np.mean(yvalues)
            currentmap3[numo2] = [avecurrentx, avecurrenty]
            totalmap[numo2] = currentmap
            #xvalues=[] ## do not reset: may 18
            #yvalues=[]
            if matchfreq[numo2] > f:
                ky = numo2
                hxvalues = xvalues
                hyvalues = yvalues
                totalmap[ky]= currentmap

            if len(hxvalues) ==0:
                print("hxvalues is len 0")
                print("f is ", f, "and matchfreq[numo2] is", matchfreq[numo2], "and numo2 is", numo2)
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

                    # May 22, 2021 : average over previous angle distances 
                    ave_prev_angle = np.mean(angles)

                    ang_diff_agg = abs(ang - ave_prev_angle)

                    print("ang diff agg is:", ang_diff_agg)

                    # 360 minus the angle difference : May 24, 2021
                    ang_diff_360 = abs(360- ang_diff_agg)

                    print("ang diff 360 is", ang_diff_360)

                    # June 2 : check if it is the same point ?
                    # x diff curr and y diff curr
                    diff_tot = abs(ydiff_curr) + abs(xdiff_curr)

                    print("diff_tot is", diff_tot)

                    if diff_tot < 5:
                        print("diff tot small, do not chec3k angles")
                        # set the rest of the params
                        prevmap= totalmap[minclust]
                        avx = mcx
                        avy =mcy
                        finalarray.append(minclust)
                        finalx.append(mcx)
                        finaly.append(mcy)
                        angles.append(ang)
                    else:
                        if ang_diff <= 35 or ang_diff_360 <=35: # change from ang_diff_agg, change from 45 to 30
                            print("angle holds")
                            prevmap= totalmap[minclust]
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
                            print("angles too large, stop unless goforward")
                            
                            if nogoforward ==1:
                                break
                            # June 21, analyze the 2,3, or 5 frames in the future
                            if goforward==0:
                                goforward=1 # skip to 2 
                                # save the fromi's
                                #prevmap -> list of fromi's 
                                fromlist =[]
                                for k in prevmap:
                                    fromlist.append(k)
                            """if goforward==1:
                                goforward=2"""
                                
                            
                            #break
                else:
                    print("not found and end unless goforward, after last frame", i)
                    # June 21 analyze 2,3,5 frames in future
                    if nogoforward==1:
                        break
                    
                    if goforward==0:
                        goforward=1
                        fromlist =[]
                        for k in prevmap:
                            fromlist.append(k)
                    """if goforward==1:
                        goforward=2"""
                    
                    #break
            if len(hxvalues) !=0:
                print("hxvalues not zero and frame is", i)
                finalarray.append(ky)
                prevmap = totalmap[ky]

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
                
            """if i % 5==0: # June 16 add map5
                #print("(map10) i is", i)
                #print("(map10) key is", ky)
                m5 = map5[i]
                m5.append(ky)
                # check sim clusts
                v1 = errorclusters.get(i)
                if v1!=None:
                    errorarray= errorclusters[i]
                    for el in errorarray:
                        for e in el:
                            if e == ky:
                                m5.extend(el)
                map5[i] = m5"""

    alen = len(finalarray)
    print("length of array ", alen)

    xv1=[]
    yv1=[]

    ax =[]
    ay =[]

    acounter=0
    for i in range(initialframe, initialframe+alen):
        name = "file_out/file_out"
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
            xarr.extend(xarray)
            yarr.extend(yarray)
            avx = np.mean(xarray)
            avy = np.mean(yarray)
            plt.annotate(i, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')

            #print("avx is for frame", i, "is:", avx)
            #print("avy is for frame ", i, "is:", avy)

            ax.append(avx)
            ay.append(avy)

        acounter =acounter +1
        if acounter > alen:
            break

    plt.show()
    arrayx_map[initialcluster] = xarr
    arrayy_map[initialcluster] = yarr
