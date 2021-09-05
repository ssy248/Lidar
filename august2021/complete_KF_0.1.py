# sept 4 change init params (matrices) of aug 3 code

# complete KF 

totalcomparisons=0
missedmatching =0
continuedmatching =0
wrongmatching=0
clustering_error=0

### input parameters
initialframe = 570
endframe = initialframe+10

n = endframe # ending frame 

c1= 1
c2 =9

mx = 15

maparrays = defaultdict(list)

for initialcluster in range(c1, c2+1):


    velx= 0.1 #avx/10
    vely= 0.1 # avy/10
    u = array(([[1], [1], [0], [0]]))
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


    pathname = "file_out/file_out"+str(initialframe)+".csv"
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
    plt.scatter(xvalues1, yvalues1)
    plt.annotate(initialframe, (avx1, avy1), textcoords="offset points", xytext=(0,10), ha='center')

    #print("start point x", avx1)
    #print("start point y", avy1)

    x1 = array(([[avx1], [avy1], [velx], [vely]])) 

    foundgreatm=0
    for i in range(initialframe+1, endframe+1): # not need to process initial frame
        pathname = "file_out/file_out"+str(i)+".csv"
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
                clusterint = int(row[0])

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
            # update for last cluster
            #update for last cluster
            mapdistances[clusterid] = currentdistances
            totxvalues[clusterid] = xvalues
            totyvalues[clusterid] = yvalues
            # find min
            for j in range(1, clusterint+1): # correct it, Aug
                meandistances = np.mean(mapdistances[j])
                if meandistances <m:
                    m = meandistances
                    ky =j
                    #print("cluster", clusters[ky])
            
            #print("final key is", ky, "for clusters as ", clusters)
            
            #outputclusters.append(clusters[ky])
            outputclusters.append(ky) 
            
            hxvalues = totxvalues[ky]
            hyvalues = totyvalues[ky]

            avx = np.mean(hxvalues)
            avy = np.mean(hyvalues)
            
            if m > 5 and foundgreatm == 0:
                curlen = len(outputclusters) # finalarray
                foundgreatm = 1

            #print("avx is", avx)
            #print("avy is", avy)

            # measurement, update
            z1 = [avx, avy]

            x1, P = update2(x1, P, z1)

            plt.scatter(hxvalues, hyvalues)
            
            plt.annotate(i, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')
            #plt.scatter(avx, avy)
            hxvalues=[]
            hyvalues=[]
            
    print("init clust", initialcluster)
    plt.show()
    maparrays[initialcluster] = outputclusters
    
    #print("our result 1 ", outputclusters)
    listclusterids = outputclusters
    
    result = []
    result.append(initialcluster)
    
    iframe = initialframe
    currentcluster = initialcluster
    t =True
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
    
    print("our result ", listclusterids)
    print(" datastore result ", result)
    
    if foundgreatm==0:
        totalcomparisons = totalcomparisons+len2 # July 30
        print("adding ", len2, " to totalcomparisons ")
    else:
        totalcomparisons = totalcomparisons +curlen
        print("adding ", curlen, " to totalcomaprisons")
            
            
        
print(" Number of total comparisons is ", totalcomparisons)
