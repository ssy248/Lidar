# try loading clusters from Cluster_frame folder
fold= '2019-9-10-12-0-0-BF1-CL1(0-18000frames)-Cluster_csv/'

arrayx_map = {}
arrayy_map = {}

initialframe=10
endframe=110

c1= 1
c2 = 6
# for loop 

for initialcluster in range(c1, c2+1):
    
    xarr =[]
    yarr= [] # June 9
    arrayx = []
    arrayy = []
    pavex = []
    pavey = []

    phx = [] # previous high x values
    phy =[] 


    obnum = 1

    totalmap ={}

    prevmap = {}

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

    for i in range(initialframe, endframe+1):
        name = fold+"Cluster_Frame"
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
                    if firstrow==0:
                        firstrow=1
                        continue
                    
                    clusterid = float(row[0])
                    if clusterid==initialcluster:
                        xpoint = float(row[2])
                        ypoint = float(row[3])
                        #print("xpt", xpoint)
                        #print("ypt", ypoint)
                        arrayx.append(xpoint)
                        arrayy.append(ypoint)
                        xr = round(xpoint)
                        yr = round(ypoint)
                        fromi = dinvlookupdict[(xr,yr)]
                        h1, i1 = dhighestfreq(fromi)
                        #i1 = newhighestfreq(fromi)
                        prevmap[i1] = 1

                        # save to matchfreq map, May 30 2021


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
            for row in csv_reader:
                
                if firstrow==0:
                    firstrow=1
                    continue
                clusterid = float(row[0])

                if clusterid != obnum:
                    numo1 = float(obnum)
                    # append into dictionary of maps
                    totalmap[numo1] = currentmap
                    if matchfreq[numo1] > f:
                        f = matchfreq[numo1] # max freq val
                        print("f is", f)
                        ky = numo1 # max freq index

                        hxvalues = xvalues
                        hyvalues = yvalues
                        hrvals = rvals

                    obnum= clusterid
                    currentmap={}
                    # take the average
                    avecurrentx = np.mean(xvalues)
                    avecurrenty = np.mean(yvalues)
                    currentmap3[numo1] = [avecurrentx, avecurrenty]

                    xvalues =[]
                    yvalues =[]
                    rvals = []

                    continue

                xpoint = float(row[2])
                ypoint = float(row[3])
                xr = round(xpoint)
                yr = round(ypoint)

                if (xr, yr) not in rvals:
                    rvals.append((xr, yr))
                    rvalindex= i

                """
                if i==16:
                    print("xr :" , xr, "yr :", yr)
                    print("xvalue:", xpoint, "yvalue:", ypoint)"""

                xvalues.append(xpoint) # save to array 
                yvalues.append(ypoint)
                fromi = dinvlookupdict[(xr,yr)]
                # function to find highest freq 
                h1, i1 = dhighestfreq(fromi)
                # save to map
                currentmap[i1] = 1
                # check prev map
                val = prevmap.get(fromi)
                if val == None:
                    pass
                else:
                    numo = float(obnum)
                    matchfreq[numo] = matchfreq[numo]+1
                    # print matchfreq

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



                    '''if mcy >20: # +y, -x
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
                            break'''

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

                    # if diff_tot is small, do not check angles (June 2)
                    if diff_tot < 5:
                        print("diff tot small")
                    else: # normal angle check
                        print("check angle")

                        if ang_diff <= 35 or ang_diff_360 <=35: # change from ang_diff, change from 45 to 30
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
                            print("angles too large, stop")
                            break
                else:
                    print("not found and end, after last frame", i)
                    break
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

    alen = len(finalarray)
    print("length of array ", alen)

    xv1=[]
    yv1=[]

    ax =[]
    ay =[]

    acounter=0
    for i in range(initialframe, initialframe+alen):
        name = fold+"Cluster_Frame"
        name = name+str(i)
        name = name+".csv"
        frow = 0

        a = finalarray[acounter]
        xarray = []
        yarray = []
        with open(name) as csv_file:
            
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                if frow==0:
                    frow=1
                    continue
                
                clusterid = float(row[0])
                xpoint = float(row[2])
                ypoint = float(row[3])

                if clusterid == a:
                    xarray.append(xpoint)
                    yarray.append(ypoint)


            # plot
            plt.scatter(xarray,yarray)
            
            xarr.extend(xarray)
            yarr.extend(yarray) # June 9
            avx = np.mean(xarray)
            avy = np.mean(yarray)
            plt.annotate(i, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')

            print("avx is for frame", i, "is:", avx)
            print("avy is for frame ", i, "is:", avy)

            ax.append(avx)
            ay.append(avy)

        acounter =acounter +1
        if acounter > alen:
            break
    plt.show()
    # June 9 save to map
    arrayx_map[initialcluster] = xarr
    arrayy_map[initialcluster] = yarr 
        
