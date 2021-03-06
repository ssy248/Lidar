# hybrid 2: angle within a range (say 45)

import math
# test for single starting cluster and frame
parrayx = []
parrayy = []

pframex = []
pframey = []

pavex = []
pavey = []
phxvalues=[]
phyvalues=[]

initialframe = 380
endframe= 390

arrayx = []
arrayy=[]

initialcluster= 1

listclusterids = []

listclusterids.append(initialcluster)

obnum = 1


totalmap={}

previndices=[]
currentindices=[]
totalmap = {}

finalarray=[]

xvalues = []
yvalues = []

hxvalues =[]
hyvalues= []

prevmap={}

mf = defaultdict(list)
# maximum object/cluster id in any frame
mx = 20

for j in range(0, mx):
    mf[j]=0 

matchfreq= mf

avex = []
avey = []

#xdiff= []
#ydiff=[]

#slopes = []

thres= 10

finalarray.append(initialcluster)

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
    
    currentmap3 = {} # average coordinates
    
    print("curr frame is:", i)
    
    with open(name) as csv_file:
        f =0 
        # reset hxvalues , hyvalues
        hxvalues = []
        hyvalues=[]
        
        obnum=1 

        currentmap= {}

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
                    h1, i1 = dhighestfreq(fromi)
                    #i1 = newhighestfreq(fromi)
                    prevmap[i1] = 1
                    
            plt.scatter(arrayx, arrayy)

            avx = np.mean(arrayx)
            avy = np.mean(arrayy)
            plt.annotate(i, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')
            # add to plot
            pframex.append(arrayx)
            pframey.append(arrayy)
            
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
                obnum = clusterid

                currentindices=[]
                currentmap= {}

                #print("clusterid is", clusterid)
                # append first values
                #xvalues.append(float(row[1]))
                #yvalues.append(float(row[2]))
                
                # take the average
                avecurrentx = np.mean(xvalues)
                avecurrenty = np.mean(yvalues)
                currentmap3[numo1] = [avecurrentx, avecurrenty]
                
                xvalues =[]
                yvalues =[]

                continue

            xpoint = float(row[1])
            ypoint = float(row[2])
            xr = round(xpoint)
            yr = round(ypoint)
            xvalues.append(xpoint) # save to array 
            yvalues.append(ypoint)
            fromi = dinvlookupdict[(xr,yr)]
            # function to find highest freq 
            h1, i1 = dhighestfreq(fromi)
            # check outlier
            freqo =0 
            ## temp comment out list outliers
            #if [xr, yr] in listoutliers:
                # determine highest outlier count + coordinates
            #    listofoutliers = listoutliers2[fromi]
            #    for outlierpt in listofoutliers:
            #        indexo = dinvlookupdict[(outlierpt[0], outlierpt[1])]
            #        ocount = doutlier[fromi, indexo]
            #        if ocount > freqo:
            #            freqo = ocount
            #            highindo = indexo
            # compare with dhighestfreq
            if freqo > h1:
                i1 = highindo
            # save to indices
            currentindices.append(i1) 
            # save to map
            currentmap[i1] = 1
            # check prev map
            val = prevmap.get(fromi)
            if val ==None:
                # do nothing
                pass
                #if search2==0:
                #    print("hi")
            else:
                numo = float(obnum)
                matchfreq[numo]= matchfreq[numo]+1
        # check f values at end of file
        numo2 = float(clusterid)
        
        # add to currentmap3 
        avecurrentx = np.mean(xvalues)
        avecurrenty = np.mean(yvalues)
        currentmap3[numo2] = [avecurrentx, avecurrenty]
        totalmap[numo2] = currentmap
        if matchfreq[numo2] > f:
            ky = numo2
            hxvalues = xvalues
            hyvalues = yvalues
            totalmap[ky]= currentmap
            
        #finalarray.append(ky)
        
        # ky is the cluster id with the highest frequency



        if len(hxvalues) ==0:
            print("0 h vals")
            # print this frame
            print("after last frame", i)
            # print previous coordinates
            #print("last x vals", phxvalues)
            #print("last y vals", phyvalues)
            # break out
            #break
            ## 
            # current diff
            
            foundmin=0
            mindist= thres
            c_first =0 
            for c in currentmap3:
                print("c:", c)
                cvalue = currentmap3[c]
                cx = cvalue[0]
                cy = cvalue[1]
                print("cx is", cx)
                print("cy is", cy)
                print("avx is", avx)
                print("avy is", avy)
                print("prev avex is", prev_avex)
                print("prev avey is", prev_avey)
                dist1 = pow(cx - avx,2) + pow(cy - avy,2)
                dist = math.sqrt(dist1)
                print("dist is", dist)
                if dist<thres:
                    if c_first ==0:
                        c_first=1
                        minclust = c
                        mcx = cx
                        mcy = cy
                    foundmin=1
                    #minclust=c
                    if dist< mindist:
                        print("dist < mindist for cluster", c)
                        mindist=dist
                        minclust = c
                        mcx =cx
                        mcy=cy
                
            if foundmin==1:
                print("foundmin")
                print("dist is", mindist)
                print("minclust is", minclust)
                
                if len(angles) ==0:
                    print("angles length 0 and minclust:", minclust)
                    prevmap = totalmap[minclust]
                    avx = mcx
                    avy = mcy 
                    finalarray.append(minclust)
                    prev_avex = avx
                    prev_avey = avy
                    plt.scatter(mcx, mcy)
                    plt.annotate(i, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')
                    continue
            
                #prev_avex = avex[-1]
                #prev_avey = avey[-1]
                
                xdiff_curr = mcx - prev_avex #how is avx set?
                ydiff_curr = mcy - prev_avey 
                print("mcx", mcx)
                print("prev avex", prev_avex)
                print("mcy", mcy)
                print("prev avey", prev_avey)
                
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
                
                if ang_diff <= 45:
                    print("angle holds")
                    prevmap= totalmap[minclust]
                    avx = mcx
                    avy =mcy
                    hxvalues = [mcx]
                    hyvalues=[mcy]
                    finalarray.append(minclust)
                    # append to slopes / diffs
                    #xdiff.append(avx - avex[-1])
                    #ydiff.append(avy - avey[-1])
                    #avex.append(avx)
                    #avey.append(avy)
            else:
                print("not found , after last frame", i)
                break
            
            
        if len(hxvalues) !=0:
            #print("not 0")
            finalarray.append(ky)
            # set prevmap to the one 
            listclusterids.append(ky) # only append if there is next match
            prevmap = totalmap[ky]
            
            avx = np.mean(hxvalues)
            avy = np.mean(hyvalues)
            # append to tempdict
            
            #td=tempdict[i]
            #td.append(ky)
            #tempdict[i] = td
            
        # obnum
        plt.scatter(hxvalues, hyvalues)
        
        # set previous x,y
        phxvalues= hxvalues
        phyvalues = hyvalues
        
        # append to ordered by frame arrays
        pframex.append(hxvalues)
        pframey.append(hyvalues)
        
        ### add to parrays
        parrayx.extend(hxvalues)
        parrayy.extend(hyvalues)

        #avx = np.mean(hxvalues)
        #avy = np.mean(hyvalues)
        
        prev_avex = avex[-1]
        prev_avey = avey[-1]
        
        avex.append(avx)
        avey.append(avy)
        
        # calc xdiff, ydiff
        xdiff = avx - prev_avex
        ydiff= avy - prev_avey
        
        r1 = math.atan2(ydiff, xdiff)
        deg1 = math.degrees(r1)
        
        if deg1<0:
            deg1 = 360+deg1
        
        angles.append(deg1)
        
        plt.annotate(i, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')
        
        prev_avex = avx
        prev_avey = avy

print("initial cluster", initialcluster)
print("initial frame", initialframe)

print("final array is", finalarray)
        
plt.show()
