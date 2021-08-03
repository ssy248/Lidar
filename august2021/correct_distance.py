# for single starting cluster
# August 1 fix -> complete

# find cluster closest to one in a frame

i = initialframe
i2 = initialframe+1
endframe=492
initialcluster = 8

name = "file_out/file_out"
name = name+str(initialframe)
name = name+".csv"



with open(name) as csv_file:
    m = 1000

    f =0 
    # reset hxvalues , hyvalues
    hxvalues = []
    hyvalues=[]

    currentmap= {}

    csv_reader = csv.reader(csv_file, delimiter=",")

    if i==initialframe:
        #print("i",i)
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
        
print("initial x is ", avx)
print("initial y is ", avy)

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
        print("mean dist is ", meandistances, " for cluster ", j)
        if meandistances < m:
            print("smaller dist", meandistances)
            print("smaller key", j)
            m = meandistances
            ky = j 
            # set avx and avy?
            hxvals = totxvalues[j]
            hyvals = totyvalues[j]
            

    print("final key is:", ky, "for frame ", i)
    
    avx = np.mean(hxvals)
    avy = np.mean(hyvals)
    print("avx is ", avx)
    print("avy is ", avy)
    m = 1000
