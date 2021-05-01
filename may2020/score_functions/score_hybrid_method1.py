# April 28 2021 
# single run , compare to score function method


initialframe =10
endframe=30

c = 3  #set c

arrayx = []
arrayy=[]

initialcluster=c

listclusterids = []

listclusterids.append(initialcluster)

obnum = 0


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

# array for counts of pts in clusters
counts = {} #[]
# normalized matchfreq scores
normalmatchfreq = mf

for i in range(initialframe, endframe+1):
    name = "file_out"
    name = name+str(i)
    name = name+".csv"
    firstrow=0
    # clear matchfreq
    for j in range(0, mx):
        matchfreq[j] =0
    with open(name) as csv_file:
        f =0 
        # reset hxvalues , hyvalues
        hxvalues = []
        hyvalues=[]

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
                    h1, i1 = highest80(fromi) # dhighestfreq(fromi)
                    #i1 = newhighestfreq(fromi)
                    # unique
                    ilist = np.unique(i1)
                    for ind1 in ilist:
                        prevmap[ind1] = 1
                    #prevmap[i1] = 1
            plt.scatter(arrayx, arrayy)

            avx1 = np.mean(arrayx)
            avy1 = np.mean(arrayy)
            plt.annotate(i, (avx1, avy1), textcoords="offset points", xytext=(0,10), ha='center')


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
                counts[numo1] = ccount
                
                normalmatchfreq[numo1] = matchfreq[numo1]/ccount
                
                if normalmatchfreq[numo1] > f: #matchfreq[numo1] > f:
                    f = normalmatchfreq[numo1]
                    print("f is", f)
                    ky = numo1

                    hxvalues = xvalues
                    hyvalues = yvalues
                obnum = clusterid

                currentindices=[]
                currentmap= {}

                xvalues =[]
                yvalues =[]
                # append first values
                #xvalues.append(float(row[1]))
                #yvalues.append(float(row[2]))
                ccount=1 

                continue

            xpoint = float(row[1])
            ypoint = float(row[2])
            xr = round(xpoint)
            yr = round(ypoint)
            
            # ccount increment
            ccount=ccount+1
            
            xvalues.append(xpoint) # save to array 
            yvalues.append(ypoint)
            fromi = dinvlookupdict[(xr,yr)]
            # function to find highest freq 
            h1, i1 = highest80(fromi) #dhighestfreq(fromi)
            #ilist = np.unique(i1)
            for ind1 in i1:
                currentmap[ind1] = 1
            # save to indices
            currentindices.append(i1) 
            # save to map
            #currentmap[i1] = 1
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
                
        # normalize matchfreq scores by number of cluster points : Apr. 28
        
        # check f values at end of file
        numo2 = float(obnum)
        counts[numo2] = ccount
        normalmatchfreq[numo2] = matchfreq[numo2]/ccount
        
        if normalmatchfreq[numo2] > f:#matchfreq[numo2] > f:
            ky = numo2
            hxvalues = xvalues
            hyvalues = yvalues
            totalmap[ky]= currentmap
        finalarray.append(ky)
        # ky is the cluster id with the highest frequency

        # add to array 
        '''
        if i % 10 == 0: # change from == endframe to % 10 ==0
            #endarray.append(ky)
            print("i", i)
            print("init cluster", c)
            print("add to array:", ky)
            earray = endarraymap[i]
            earray.append(ky)
            endarraymap[i] = earray
        '''    

        if len(hxvalues) ==0:
            print("0 h vals")
            # break out
            break
        if len(hxvalues) !=0:
            #print("not 0")
            # set prevmap to the one 
            listclusterids.append(ky) # only append if there is next match
            prevmap = totalmap[ky]
        # obnum
        plt.scatter(hxvalues, hyvalues)

        #totalplottingx.extend(hxvalues)
        #totalplottingy.extend(hyvalues)

        avx = np.mean(hxvalues)
        avy = np.mean(hyvalues)
        plt.annotate(i, (avx, avy), textcoords="offset points", xytext=(0,10), ha='center')


plt.show()
#print("our res. array for initial cluster",c, ":", listclusterids)

currentframe = initialframe

#initialcluster 
print("our array,", listclusterids)
