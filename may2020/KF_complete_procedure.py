# complete 3



### input parameters
initialframe = 50
endframe = 60

n = endframe # ending frame 

c1= 1
c2 = 8

maparrays = defaultdict(list)

for initialcluster in range(1, c2+1):


    velx= avx/10
    vely=avy/10
    u = array(([[4.0], [12.0], [0], [0]]))
    P = array([[10, 0, 0 , 0], [0, 10, 0, 0], [0, 0, 100, 0], [0, 0, 0, 100]])
    F = array([[1, 0, dt , 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]])
    H = array([[1,0,0,0], [0,1,0,0]])
    # meas noise
    R = array([[0.1,0], [0,0.1]])
    B = np.eye(4)
    Q = np.eye(4)


    # parameters of step 5


    obnum =1


    xvalues = []
    yvalues = []

    hxvalues =[]
    hyvalues= []


    # initialize distances map 
    mapdistances = defaultdict(list)

    totxvalues = defaultdict(list)
    totyvalues = defaultdict(list)


    currentcluster = 0
    clusters = defaultdict(list)

    f = 1000 # default value

    for j in range(0, mx):
        mapdistances[j]=[]
        totxvalues[j] = []
        totyvalues[j] = []
        clusters[j] = []

    currentdistances = []


    outputclusters = []
    outputclusters.append(initialcluster)


    pathname = "file_out"+str(initialframe)+".csv"
    firstrow=0

    xvalues1= []
    yvalues1 = []

    with open(pathname) as csv_file:
        m = f
        currentmap={}
        csv_reader = csv.reader(csv_file, delimiter=",")

        for row in csv_reader:
            # don't skip first row
            clusterid = float(row[0])
            xpoint = float(row[1])
            ypoint = float(row[2])
            if clusterid == initialcluster:
                xvalues1.append(xpoint)
                yvalues1.append(ypoint)
    # find x1 based on icluster 
    avx1 = np.mean(xvalues1)
    avy1 = np.mean(yvalues1)

    #print("start point x", avx1)
    #print("start point y", avy1)

    x1 = array(([[avx1], [avy1], [velx], [vely]])) 


    for i in range(initialframe+1, endframe): # not need to process initial frame
        pathname = "file_out"+str(i)+".csv"
        firstrow=0
        for j in range(0, mx):
            mapdistances[j]= []
            totxvalues[j]= []
            totyvalues[j]= []
            clusters[j] = []
        # predict
        x1, P = predict1(x1, P)

        with open(pathname) as csv_file:
            m = f
            currentmap={}
            csv_reader = csv.reader(csv_file, delimiter=",")

            for row in csv_reader:
                # don't skip first row
                clusterid = float(row[0])

                if clusterid != obnum:
                    numo1 = float(obnum)
                    mapdistances[numo1] = currentdistances
                    totxvalues[numo1] = xvalues
                    totyvalues[numo1] = yvalues
                    clusters[numo1] = currentcluster
                    obnum = clusterid
                    currentdistances=[]
                    xvalues=[]
                    yvalues=[]
                    continue

                xpoint = float(row[1])
                ypoint = float(row[2])
                xvalues.append(xpoint)
                yvalues.append(ypoint)
                currentcluster = clusterid

                #print("x1", x1)
                #print("x1[0]", x1[0])

                # distance from predicted point x1
                dx1 = x1[0] - xpoint
                dy1 = x1[1] - ypoint
                d1 = pow(dx1,2)+pow(dy1,2)
                dist = math.sqrt(d1)
                # save
                currentdistances.append(dist)
            # find min
            for j in range(0, mx):
                meandistances = np.mean(mapdistances[j])
                if meandistances <m:
                    m = meandistances
                    ky =j
                    #print("cluster", clusters[ky])

            outputclusters.append(clusters[ky])
            hxvalues = totxvalues[ky]
            hyvalues = totyvalues[ky]

            avx = np.mean(hxvalues)
            avy = np.mean(hyvalues)

            #print("avx is", avx)
            #print("avy is", avy)

            # measurement, update
            z1 = [avx, avy]

            x1, P = update2(x1, P, z1)

            plt.scatter(hxvalues, hyvalues)
            #plt.scatter(avx, avy)
            hxvalues=[]
            hyvalues=[]
            
    print("init clust", initialcluster)
    plt.show()
    maparrays[initialcluster] = outputclusters
            
            
        
# analyze

for initialcluster in range(c1, c2+1):
    listclusterids = maparrays[initialcluster]
    result =[]
    result.append(initialcluster)
    iframe = initialframe
    currentcluster = initialcluster
    t = True
    while t:
        nextres = findnextclusterapp(iframe, currentcluster)
        if str(nextres) == "nan":
            break
        if nextres==0:
            break 
        if iframe > endframe: 
            break
        result.append(nextres)
        iframe = iframe+1
        currentcluster = nextres
    len1 = len(result)
    len2 = len(listclusterids)
    setlen = min(len1, len2)
    od1 = {}
    od2 = {}
    booleanwrong = []
    for j1 in range(0,setlen):
        nolongerwrong=0
        nolongerwrongoriginal=0
        frameno = initialframe + j1
        od1[frameno] = [result[j1]]
        od2[frameno] =[listclusterids[j1]]
        if result[j1]==listclusterids[j1]:
            nolongerwrong=1
            nolongerwrongoriginal=1
        if result[j1] != listclusterids[j1]:
            v1 = errorclusters.get(frameno)
            if v1 != None:
                errorarray = errorclusters[frameno]
                for el in errorarray:
                    if result[j1] in el:
                        if listclusterids[j1] in el:
                            nolongerwrong=1
        if nolongerwrong!= 1:
            booleanwrong.append(1) 
        else:
            booleanwrong.append(0)
            if nolongerwrongoriginal==0:
                clustering_error = clustering_error+1
    maxlen = max(len1, len2)
    last1 = result[setlen-1]
    last2 = listclusterids[setlen-1]
    if len1 != len2:
        for j2 in range(setlen, maxlen):
            nolongerwrong=0
            nolongerwrongoriginal=0
            frameno2 = initialframe+j2
            if len1>len2:
                next2 = findnextclusterKF(frameno2, last2, P)
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
                    if nolongerwrongoriginal==0:
                        clustering_error = clustering_error+1
                else:
                    booleanwrong.append(1)
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
                        clustering_error= clustering_error+1
                else:
                    booleanwrong.append(1) # wrong
    d1 = {}
    d2 = {}
    for j1 in range(0, setlen):
        frameno = initialframe+j1
        clusters1 = od1[frameno]
        clusters2 = od2[frameno]
        simclusters = errorclusters.get(frameno)
        if simclusters!=None:
            simarray = errorclusters[frameno]
            for el in simarray:
                if od1[frameno] in el:
                    clusters1.extend(el)
                if od2[frameno] in el:
                    clusters2.extend(e1)
        d1[frameno] = clusters1
        d2[frameno] = clusters2
    maxlen = max(len1, len2)
    for j2 in range(setlen, maxlen):
        frameno = initialframe+j2
        d1[frameno] = []
        d2[frameno] = []
        if len1>len2:
            d1[frameno] = [result[j2]]
        if len2>len1:
            d2[frameno]= [listclusterids[j2]]
    d1[initialframe+maxlen] =[]
    d2[initialframe+maxlen]=[]
    setlen= min(len1, len2)
    for j in range(0, maxlen):
        frameno = initialframe+j
        clust1= d1[frameno]
        clust2 = d2[frameno]
        for c1 in clust1:
            nc1 = findnextclusterapp(frameno, c1)
            if str(nc1) =="nan":
                print("nc1 is nan")
                continue
            nclust1 = d1[frameno+1]
            if nc1 not in nclust1:
                nclust1.append(nc1) 
            d1[frameno+1] = nclust1
        for c2 in clust2:
            nc2 = findnextclusterKF(frameno, c2, P)
            if nc2==-1:
                continue
            if str(nc2) == "nan":
                continue
            nclust2 = d2[frameno+1]
            if nc2 not in nclust2:
                nclust2.append(nc2)
            d2[frameno+1]= nclust2
        if booleanwrong[j] ==1:
            set1=set(clust1)
            intersect= set1.intersection(clust2)
            if len(intersect)>0:
                booleanwrong[j]=0
                clustering_error=clustering_error+1
    bindex=1
    firstframewrong=-1
    for b in booleanwrong:
        if b==1:
            firstframewrong=bindex
            break
        bindex=bindex+1
    if firstframewrong==-1:
        totalcomparisons= totalcomparisons+maxlen
    else:
        totalcomparisons=totalcomparisons+firstframewrong
        
    contflag=0
    missedflag=0
    
    if np.sum(booleanwrong) >0:
        if firstframewrong>len1:
            print("continued")
            print("array1", result)
            print("array2", listclusterids)
            contflag=1
            continuedmatching=continuedmatching+1
        if firstframewrong > len2:
            print("missed")
            print("array1", result)
            print("array2", listclusterids)
            missedmatching= missedmatching+1
            missedflag=1
        if contflag==0 and missedflag==0:
            print("wrong")
            print("array1", result)
            print("array2", listclusterids)
            wrongmatching= wrongmatching+1
        if contflag==1 and missedflag==1:
            print("BOTH CONTINUED and MISSED")
        
                    
                
