# August 2  : complete
c1 =1
c2 = 6

missedmatching=0
continuedmatching=0
wrongmatching=0
clustering_error = 0
totalcomparisons = 0

totalcomparisons2 =0
initialframe =110
endframe = 120

icont = []
iwrong = []
imissed = []
m =100

for c in range(c1, c2+1):
    print("current cluster is", c)
    initialcluster = c
    # array to be plotted
    arrayx = []

    arrayy = []

    xvalues = []
    yvalues = []

    finalarray=[]
    
    finalarray.append(initialcluster)

    totxvalues = defaultdict(list)
    totyvalues = defaultdict(list)
    # initialize distances map 
    mapdistances = defaultdict(list)

    obnum =0

    currentdistances = []
    
    listclusterids=[]
    
    name = "file_out/file_out"
    name = name+str(initialframe)
    name = name+".csv"

    with open(name) as csv_file:

        f =0 
        # reset hxvalues , hyvalues
        hxvalues = []
        hyvalues=[]

        currentmap= {}

        csv_reader = csv.reader(csv_file, delimiter=",")

        for row in csv_reader:

            clusterid = float(row[0])

            #print("clusterid", clusterid)
            if clusterid==initialcluster:
                xpoint = float(row[1])
                ypoint = float(row[2])
                arrayx.append(xpoint)
                arrayy.append(ypoint)

        # find average 
        avx = np.mean(arrayx)
        avy = np.mean(arrayy)
        plt.scatter(arrayx, arrayy)
        plt.annotate(initialframe, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')

    
        
    foundgreatm =0
    
    for i in range(initialframe+1, endframe+1):
    
        name2 = "file_out/file_out"
        name2 = name2+str(i)
        name2 = name2+".csv"
        firstrow=0
        # clear map
        mxvalmap=15
        for j in range(0, mxvalmap):
            mapdistances[j] =[]
            totxvalues[j] =[]
            totyvalues[j]=[]

        with open(name2) as csv_file2:
            csv_reader2 =csv.reader(csv_file2, delimiter=",")

            for row in csv_reader2:
                clusterid = float(row[0]) # current cluster id 
                clusterint = int(row[0])
                if clusterid != obnum:
                    numo1 = float(obnum)
                    mapdistances[numo1] = currentdistances
                    totxvalues[numo1] = xvalues
                    totyvalues[numo1] = yvalues
                    # new comparisons 
                    obnum = clusterid

                    currentdistances=[]
                    #currentmap= {}

                    xvalues =[]
                    yvalues =[]

                    continue
                xpoint = float(row[1])
                ypoint = float(row[2])
                xvalues.append(xpoint) # save to array 
                yvalues.append(ypoint)
                # calc distance
                dx1 = avx - xpoint
                dy1 = avy - ypoint
                d1 = pow(dx1, 2) + pow(dy1, 2)
                dist = pow(d1, 0.5)
                currentdistances.append(dist)
        #update for last cluster
        mapdistances[clusterid] = currentdistances
        totxvalues[clusterid] = xvalues
        totyvalues[clusterid] = yvalues
        # change mx to the max of # clusters

        for j in range(1, clusterint+1):
            meandistances = np.mean(mapdistances[j])
            #print("mean dist is ", meandistances, " for cluster ", j)
            if meandistances < m:
                #print("smaller dist", meandistances)
                #print("smaller key", j)
                m = meandistances
                ky = j 
                # set avx and avy?
                hxvals = totxvalues[j]
                hyvals = totyvalues[j]


        #print("final key is:", ky, "for frame ", i)

        avx = np.mean(hxvals)
        avy = np.mean(hyvals)
        #print("avx is ", avx)
        #print("avy is ", avy)
        if m > 5 and foundgreatm == 0:
            curlen = len(finalarray)
            foundgreatm = 1
                
        finalarray.append(ky)
        hxvalues = totxvalues[ky]
        hyvalues = totyvalues[ky]

        avx = np.mean(hxvalues)
        avy = np.mean(hyvalues)

        plt.scatter(hxvalues, hyvalues)
        plt.annotate(i, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')
        
        m = 1000
    plt.show()
    
    print("our final array is ", finalarray)
    
    listclusterids = finalarray
    
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
    
    if foundgreatm==0:
        totalcomparisons = totalcomparisons+len2 # July 30
        print("adding ", len2, " to totalcomparisons ")
    else:
        totalcomparisons = totalcomparisons +curlen
        print("adding ", curlen, " to totalcomaprisons")
